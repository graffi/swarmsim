"""
Configuration utility module for saving and loading presets to config.ini
"""

import configparser
import os


def save_config_preset(preset, randomize_seed=True):
    """
    Save a preset configuration to config.ini
    
    Args:
        preset: dict with sim_type, scenario, solution
        randomize_seed: if True, increment seed by 1 for variety in simulations
    """
    config_file = "config.ini"
    config = configparser.ConfigParser(allow_no_value=True)
    
    if os.path.exists(config_file):
        config.read(config_file)
    
    # Ensure Simulator section exists
    if not config.has_section("Simulator"):
        config.add_section("Simulator")
    
    # Update configuration values
    config.set("Simulator", "sim_type", preset.get("sim_type", "gravity"))
    config.set("Simulator", "scenario", preset.get("scenario", "lowered_mid"))
    config.set("Simulator", "solution", preset.get("solution", "gravity_christophebert"))
    
    # Optionally randomize seed for different simulations
    if randomize_seed:
        try:
            current_seed = config.getint("Simulator", "seed_value")
            new_seed = current_seed + 1
            config.set("Simulator", "seed_value", str(new_seed))
        except (configparser.NoOptionError, ValueError):
            # If seed not found or invalid, just use default
            pass
    
    # Write back to file
    with open(config_file, 'w') as f:
        config.write(f)


def load_current_config():
    """
    Load current configuration from config.ini
    
    Returns:
        dict with sim_type, scenario, solution, seed_value
    """
    config_file = "config.ini"
    config = configparser.ConfigParser(allow_no_value=True)
    
    if os.path.exists(config_file):
        config.read(config_file)
    
    return {
        "sim_type": config.get("Simulator", "sim_type", fallback="gravity"),
        "scenario": config.get("Simulator", "scenario", fallback="lowered_mid"),
        "solution": config.get("Simulator", "solution", fallback="gravity_christophebert"),
        "seed_value": config.getint("Simulator", "seed_value", fallback=10),
    }
