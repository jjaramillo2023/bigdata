"""
crime_categories.py
────────────────────────────────────────────────
Shared category map used by both city ETL scripts.

Maps each city's raw crime labels to one standardized
category so both SQL tables use the same vocabulary.

Add new mappings here if you find unmapped crime types
after running the ETL (they'll show up as "Other").
────────────────────────────────────────────────
"""

CRIME_CATEGORY_MAP = {
    # ── Seattle (NIBRS labels) ──────────────────
    "LARCENY-THEFT":              "Theft",
    "BURGLARY":                   "Burglary",
    "MOTOR VEHICLE THEFT":        "Vehicle Theft",
    "ROBBERY":                    "Robbery",
    "ASSAULT OFFENSES":           "Assault",
    "HOMICIDE OFFENSES":          "Homicide",
    "DRUG/NARCOTIC OFFENSES":     "Drugs",
    "VANDALISM":                  "Vandalism",
    "FRAUD OFFENSES":             "Fraud",
    "TRESPASS OF REAL PROPERTY":  "Trespassing",
    "WEAPON LAW VIOLATIONS":      "Weapons",
    "SEX OFFENSES":               "Sex Offenses",
    "ARSON":                      "Arson",

    # ── Chicago (Primary Type labels) ───────────
    "THEFT":                      "Theft",
    "BURGLARY":                   "Burglary",
    "MOTOR VEHICLE THEFT":        "Vehicle Theft",
    "ROBBERY":                    "Robbery",
    "ASSAULT":                    "Assault",
    "BATTERY":                    "Assault",       # Chicago uses Battery; maps to Assault
    "HOMICIDE":                   "Homicide",
    "NARCOTICS":                  "Drugs",
    "CRIMINAL DAMAGE":            "Vandalism",
    "DECEPTIVE PRACTICE":         "Fraud",
    "CRIMINAL TRESPASS":          "Trespassing",
    "WEAPONS VIOLATION":          "Weapons",
    "SEX OFFENSE":                "Sex Offenses",
    "ARSON":                      "Arson",
    "OTHER OFFENSE":              "Other",
}