from lib.oppnet.messagestore import MessageStore
from lib.oppnet.mobility_model import MobilityModel
from lib.particle import Particle


class Particle(Particle):
    def __init__(self, world, coordinates, color, particle_counter=0, csv_generator=None, ms_size=None,
                 ms_strategy=None, mm_mode=None, mm_length=None, mm_zone=None, mm_starting_dir=None):
        super().__init__(world=world, coordinates=coordinates, color=color, particle_counter=particle_counter,
                         csv_generator=csv_generator)

        self.mobility_model = None
        self.routing_parameters = None

        if not ms_size:
            ms_size = world.particle_ms_size
        if not ms_strategy:
            ms_strategy = world.particle_ms_strategy

        if not mm_mode:
            mm_mode = world.particle_mm_mode
        if not mm_length:
            mm_length = world.particle_mm_length
        if not mm_zone:
            mm_zone = world.particle_mm_zone
        if not mm_starting_dir:
            mm_starting_dir = world.particle_mm_starting_dir

        self.__init_message_stores__(ms_size, ms_strategy)
        self.__init_mobility_model__(mm_mode, mm_length, mm_zone, mm_starting_dir)

        self.routing_parameters = world.routing_parameters

        self.signal_velocity = 1

    def __init_message_stores__(self, ms_size, ms_strategy):
        self.send_store = MessageStore(maxlen=ms_size, strategy=ms_strategy)
        self.rcv_store = MessageStore(maxlen=ms_size, strategy=ms_strategy)

    def __init_mobility_model__(self, mm_mode, length, zone, starting_dir):
        m_model = MobilityModel(self.coordinates[0], self.coordinates[1], mm_mode, length, zone, starting_dir)
        self.mobility_model = m_model

    def set_mobility_model(self, mobility_model):
        self.mobility_model = mobility_model

    def set_routing_parameters(self, routing_parameters):
        self.routing_parameters = routing_parameters
