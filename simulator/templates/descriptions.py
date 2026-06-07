#text templates (Groq generetated)

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