OPERATOR_NAMES = [
    "Janko Rakonjac", "Bozidar Rakonjac", "Aleksandar Pavlovic",
    "Mateja Rilak", "Nemanja Pokornic", "Ivan Gojevic", "Luka Demeter", "Jovan Drobnjak"
]

DOWNTIME_DESCRIPTIONS = {
    "TOOL_WEAR_FAILURE":  "Machine halted due to excessive tool wear. Tool replacement required.",
    "HEAT_FAILURE":       "Machine stopped due to heat dissipation failure. Temperature exceeded threshold.",
    "POWER_FAILURE":      "Emergency stop triggered by power failure. Voltage drop detected.",
    "OVERSTRAIN_FAILURE": "Machine stopped due to overstrain on spindle. Load exceeded limits.",
    "RANDOM_FAILURE":     "Unexpected failure detected. Cause under investigation by technician."
}

REASON_CODES = {
    "TOOL_WEAR_FAILURE":  "TOOL_WEAR",
    "HEAT_FAILURE":       "OVERHEAT",
    "POWER_FAILURE":      "POWER_FAULT",
    "OVERSTRAIN_FAILURE": "OVERSTRAIN",
    "RANDOM_FAILURE":     "UNKNOWN"
}

DEFECT_TYPES = [
    "SURFACE_SCRATCH",
    "DIMENSION_ERROR",
    "WEIGHT_DEVIATION",
    "COLOR_MISMATCH",
    "ASSEMBLY_FAULT",
    "BURR_FORMATION",
    "POROSITY",
    "MISALIGNMENT",
    "CONTAMINATION",
    "CRACK_DETECTED",
    "TOOL_MARK",
    "ROUGH_SURFACE",
    "EDGE_CHIPPING",
    "DEFORMATION",
    "HOLE_POSITION_ERROR"
]

QUALITY_DESCRIPTIONS = {
    "SURFACE_SCRATCH":      "Linear scratches found on product surface. Likely caused by worn conveyor belt contact points.",
    "DIMENSION_ERROR":      "Product dimensions outside tolerance. Width measured over specification limit.",
    "WEIGHT_DEVIATION":     "Product weight below minimum threshold. Possible material feed inconsistency detected.",
    "COLOR_MISMATCH":       "Product color outside acceptable range. Paint mixture inconsistency detected.",
    "ASSEMBLY_FAULT":       "Assembly misalignment detected. Component positioning outside tolerance.",
    "BURR_FORMATION":       "Sharp metal burrs found on edges. Tool wear likely cause. Deburring required.",
    "POROSITY":             "Small voids detected inside material. Casting process inconsistency suspected.",
    "MISALIGNMENT":         "Component misalignment detected during inspection. Fixture positioning issue.",
    "CONTAMINATION":        "Foreign material found on product surface. Coolant contamination suspected.",
    "CRACK_DETECTED":       "Micro cracks detected on product body. Material stress during processing.",
    "TOOL_MARK":            "Tool marks visible on finished surface. Feed rate too high during machining.",
    "ROUGH_SURFACE":        "Surface roughness exceeds specification. Cutting parameters need adjustment.",
    "EDGE_CHIPPING":        "Chipping detected on product edges. Brittle material behavior during cutting.",
    "DEFORMATION":          "Product shape deformed beyond tolerance. Clamping pressure too high.",
    "HOLE_POSITION_ERROR":  "Drilled hole position outside tolerance. CNC coordinate offset detected."
}

# Realistic mapping - which failure causes which defects
FAILURE_TO_DEFECT_MAP = {
    "TOOL_WEAR_FAILURE":  ["SURFACE_SCRATCH", "BURR_FORMATION", "ROUGH_SURFACE", "EDGE_CHIPPING", "TOOL_MARK"],
    "HEAT_FAILURE":       ["DEFORMATION", "COLOR_MISMATCH", "CRACK_DETECTED", "POROSITY"],
    "POWER_FAILURE":      ["MISALIGNMENT", "HOLE_POSITION_ERROR", "ASSEMBLY_FAULT", "DIMENSION_ERROR"],
    "OVERSTRAIN_FAILURE": ["DEFORMATION", "CRACK_DETECTED", "DIMENSION_ERROR", "WEIGHT_DEVIATION"],
    "RANDOM_FAILURE":     ["CONTAMINATION", "POROSITY", "WEIGHT_DEVIATION", "SURFACE_SCRATCH"]
}