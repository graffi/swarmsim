"""
Configuration presets for working simulation combinations.

Each preset defines a valid combination of sim_type, scenario, and solution.
This prevents users from selecting broken configuration combinations.
"""

PRESETS = {
    "Gravity": [
        {
            "id": "gravity_christophebert_lowered_mid",
            "name": "Gravity - Christophebert (Lowered Mid)",
            "description": "Particles settle and form towers using gravity-based algorithm",
            "sim_type": "gravity",
            "scenario": "lowered_mid",
            "solution": "gravity_christophebert",
            "working": True,
        },
        {
            "id": "gravity_christophebert_elevated_mid",
            "name": "Gravity - Christophebert (Elevated Mid)",
            "description": "Particles settle from elevated middle using gravity algorithm",
            "sim_type": "gravity",
            "scenario": "elevated_mid",
            "solution": "gravity_christophebert",
            "working": True,
        },
        {
            "id": "gravity_christophebert_three_islands",
            "name": "Gravity - Christophebert (Three Islands)",
            "description": "Particles settle on three island formations",
            "sim_type": "gravity",
            "scenario": "three_islands",
            "solution": "gravity_christophebert",
            "working": True,
        },
        {
            "id": "gravity_christophebert_three_islands_holes",
            "name": "Gravity - Christophebert (Three Islands with Holes)",
            "description": "Particles settle on three islands with holes",
            "sim_type": "gravity",
            "scenario": "three_islands_holes",
            "solution": "gravity_christophebert",
            "working": True,
        },
        {
            "id": "gravity_christophebert_small_single",
            "name": "Gravity - Christophebert (Small Single)",
            "description": "Small single island scenario with gravity algorithm",
            "sim_type": "gravity",
            "scenario": "small_single",
            "solution": "gravity_christophebert",
            "working": True,
        },
        {
            "id": "gravity_tentacle_lowered_mid",
            "name": "Gravity - Tentacle (Lowered Mid)",
            "description": "Particles settle using tentacle-based movement strategy",
            "sim_type": "gravity",
            "scenario": "lowered_mid",
            "solution": "gravity_tentacle",
            "working": True,
        },
    ],
    "Random Walk": [
        {
            "id": "master_n_agent_line",
            "name": "Random Walk - N Agents in Line",
            "description": "Agents perform random walk in a line formation",
            "sim_type": "master",
            "scenario": "n_agent_in_line",
            "solution": "random_walk",
            "working": True,
        },
    ],
    "Coating": [
        {
            "id": "coating_bottle",
            "name": "Coating - Bottle Scenario",
            "description": "General coating algorithm on bottle-shaped scenario",
            "sim_type": "coating",
            "scenario": "bottle",
            "solution": "p_max_lifetime.main",
            "working": True,
        },
    ],
    "3D Marking": [
        {
            "id": "3d_marking_marking_3d",
            "name": "3D Marking - Marking 3D Scenario",
            "description": "3D particle marking with local coordination",
            "sim_type": "3D",
            "scenario": "marking_3d_scenario",
            "solution": "marking_3d_local",
            "working": True,
        },
    ],
    "Test": [
        {
            "id": "master_test_interfaces",
            "name": "Test - All Interfaces",
            "description": "Test all simulation interfaces",
            "sim_type": "master",
            "scenario": "test_interfaces",
            "solution": "test_all_the_interfaces",
            "working": True,
        },
    ],
}


def get_all_presets():
    """Return all available presets organized by category."""
    return PRESETS


def get_presets_by_category(category):
    """Get presets for a specific category."""
    return PRESETS.get(category, [])


def get_all_categories():
    """Return all available category names."""
    return list(PRESETS.keys())


def get_preset_by_id(preset_id):
    """Find a preset by its ID."""
    for category in PRESETS.values():
        for preset in category:
            if preset["id"] == preset_id:
                return preset
    return None


def find_preset(sim_type, scenario, solution):
    """Find a preset matching the given configuration."""
    for category in PRESETS.values():
        for preset in category:
            if (preset["sim_type"] == sim_type and
                preset["scenario"] == scenario and
                preset["solution"] == solution):
                return preset
    return None
