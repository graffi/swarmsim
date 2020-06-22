import collections
import logging

from lib.oppnet.communication import Message
from lib.oppnet.message_types import LeaderMessageType, LeaderMessageContent, SafeLocationMessage, LostMessageContent, \
    LostMessageType
from lib.oppnet.mobility_model import MobilityModelMode, MobilityModel
from lib.oppnet.particles import FlockMode


class Mixin:
    def __process_as_follower__(self, received_messages: [Message]):
        self.__add__new_contacts_as_follower__(received_messages)
        for message in received_messages:
            content = message.get_content()
            if isinstance(content, LeaderMessageContent):
                message_type = content.message_type
                if message_type == LeaderMessageType.instruct:
                    self.__process_instruct_as_follower__(message)
                elif message_type == LeaderMessageType.discover:
                    self.send_to_leader_via_contacts(message, content.receivers.pop())
                elif message_type in [LeaderMessageType.discover_ack, LeaderMessageType.commit]:
                    self.send_to_leader_via_contacts(message, receiving_leader=message.get_actual_receiver())
                else:
                    self.send_to_leader_via_contacts(message)
            elif isinstance(content, LostMessageContent):
                self.__process_lost_message_as_follower__(message)
            elif isinstance(content, SafeLocationMessage):
                self.__process_safe_location_message_as_follower(message)

    def __add__new_contacts_as_follower__(self, received_messages):
        for message in received_messages:
            if isinstance(message.get_content(), LeaderMessageContent):
                sending_leader = message.get_content().sending_leader
                if sending_leader not in self.leader_contacts:
                    self.__add_route__(message.get_sender(), sending_leader, message.get_hops(), is_leader=True)
                    logging.debug(
                        "round {}: opp_particle -> particle #{} found a new leader #{} with {} hops."
                            .format(self.world.get_actual_round(), self.number, sending_leader.number,
                                    message.get_hops()))
                if message.get_original_sender() not in self.leader_contacts:
                    self.__add_route__(message.get_sender(), message.get_original_sender(), message.get_hops(),
                                       is_leader=True)
            else:
                self.__add_route__(message.get_sender(), message.get_original_sender(), message.get_hops(),
                                   is_leader=False)

    def __process_instruct_as_follower__(self, message: Message):
        self.__update__instruct_round_as_follower_(message)
        logging.debug("round {}: opp_particle -> particle {} received instruct # {}".format(
            self.world.get_actual_round(), self.number, self._instruction_number_))
        self.__flood_forward__(message)

    def __update__instruct_round_as_follower_(self, received_message: Message):
        content = received_message.get_content()
        new_instruction_round = self.world.get_actual_round() + content.t_wait
        instruction_number = content.number
        if self._instruction_number_ is None or (instruction_number > self._instruction_number_):
            self.instruct_round = new_instruction_round
            self.proposed_direction = content.proposed_direction
            self._current_instruct_message = received_message
            self._instruction_number_ = instruction_number
            self.t_wait = content.t_wait
            self.mobility_model.set_mode(MobilityModelMode.Manual)

    def __process_lost_message_as_follower__(self, message: Message):
        content = message.get_content()
        message_type = content.message_type
        if message_type == LostMessageType.RejoinMessage and message.get_actual_receiver() == self:
            self.mobility_model = MobilityModel(self.coordinates, MobilityModelMode.POI,
                                                poi=content.get_current_location())
        elif message_type == LostMessageType.SeparationMessage:
            self.leader_contacts.remove_all_entries_with_particle(message.get_original_sender())
            self.follower_contacts.remove_all_entries_with_particle(message.get_original_sender())
        elif message_type == LostMessageType.QueryNewLocation:
            self.flood_message_content(content)
            self.__add_route__(message.get_sender(), message.get_original_sender(), message.hops, is_leader=False)
            free_locations = self.get_free_surrounding_locations()
            self.send_message_content_via_contacts(message.get_original_sender(),
                                                   LostMessageContent(LostMessageType.FreeLocations,
                                                                      free_locations=free_locations))
            setattr(self, 'query_location_round', self.world.get_actual_round())
        elif message_type == LostMessageType.FreeLocations and message.get_actual_receiver() == self:
            free_locations = getattr(self, 'free_locations', collections.Counter())
            for location in content.get_free_locations():
                free_locations[location] += 1
            setattr(self, 'free_locations', free_locations)

    def __process_safe_location_message_as_follower(self, message):
        content = message.get_content()
        if self.flock_mode != FlockMode.Flocking or not message.is_broadcast:
            self.mobility_model.set_mode(MobilityModelMode.POI)
            self.mobility_model.poi = content.coordinates
            self.proposed_direction = self.mobility_model.next_direction(self.coordinates)