import pandas as pd

# Training dataset — 50 suppliers with features and known risk labels
# Features: country_risk, lead_time, rating, price_volatility, capacity_util, geopolitical_score
# Label: risk_score (0-100)

SUPPLIERS_DATA = [
    # name, country, material, country_risk, lead_time, rating, price_vol, capacity_util, geo_score, risk_score
    ("NeoChip Taiwan",    "Taiwan",  "Semiconductors", 75, 18, 4.2, 0.72, 0.88, 78, 82),
    ("SinoElec Corp",     "China",   "Semiconductors", 82, 22, 3.7, 0.81, 0.91, 85, 91),
    ("VoltPath India",    "India",   "Semiconductors", 30, 12, 4.6, 0.35, 0.72, 28, 31),
    ("TexasIC USA",       "USA",     "Semiconductors", 20, 9,  4.8, 0.20, 0.68, 18, 24),
    ("EuroSemi GmbH",     "Germany", "Semiconductors", 15, 14, 4.5, 0.22, 0.75, 14, 18),
    ("LithoCo Korea",     "Korea",   "Battery Metals", 40, 20, 4.1, 0.48, 0.80, 42, 44),
    ("CopperLane Chile",  "Chile",   "Battery Metals", 35, 25, 3.9, 0.55, 0.65, 32, 37),
    ("MineX Congo",       "Congo",   "Battery Metals", 80, 35, 3.2, 0.88, 0.70, 82, 78),
    ("AutoSteel DE",      "Germany", "Steel",          15, 11, 4.7, 0.18, 0.78, 12, 22),
    ("SteelIndia Ltd",    "India",   "Steel",          28, 13, 4.4, 0.30, 0.74, 25, 29),
    # Additional training rows for model quality
    ("RussoMetal",        "Russia",  "Steel",          92, 40, 2.8, 0.95, 0.60, 95, 96),
    ("SafeSource UK",     "UK",      "Semiconductors", 18, 15, 4.6, 0.21, 0.70, 16, 20),
    ("JapanTech",         "Japan",   "Semiconductors", 22, 16, 4.7, 0.25, 0.76, 20, 25),
    ("IranPetro",         "Iran",    "Plastics",       95, 50, 2.5, 0.98, 0.55, 98, 97),
    ("CanadaMine",        "Canada",  "Battery Metals", 16, 20, 4.5, 0.22, 0.72, 15, 19),
    ("AusMinerals",       "Australia","Battery Metals",18, 22, 4.4, 0.24, 0.68, 17, 21),
    ("BrazilSteel",       "Brazil",  "Steel",          45, 28, 3.8, 0.52, 0.66, 44, 48),
    ("MexicoAuto",        "Mexico",  "Steel",          38, 18, 4.0, 0.44, 0.74, 36, 40),
    ("VietnamTech",       "Vietnam", "Semiconductors", 35, 20, 4.1, 0.40, 0.78, 33, 36),
    ("ThaiSource",        "Thailand","Semiconductors", 32, 18, 4.2, 0.38, 0.76, 30, 34),
    ("NordicComp",        "Sweden",  "Semiconductors", 12, 14, 4.8, 0.18, 0.71, 11, 15),
    ("SwissPrec",         "Switzerland","Semiconductors",10,13,4.9,0.15,0.69,9,13),
    ("PolandMfg",         "Poland",  "Steel",          28, 16, 4.3, 0.32, 0.73, 26, 30),
    ("TurkeyMetal",       "Turkey",  "Steel",          55, 24, 3.6, 0.62, 0.68, 54, 58),
    ("UkraineSteel",      "Ukraine", "Steel",          90, 45, 2.6, 0.93, 0.50, 92, 95),
    ("ArgentineLi",       "Argentina","Battery Metals", 50, 30, 3.5, 0.60, 0.62, 48, 52),
    ("BoliviaLi",         "Bolivia", "Battery Metals", 58, 32, 3.3, 0.65, 0.58, 56, 60),
    ("NamibiaRare",       "Namibia", "Rare Earths",    45, 35, 3.7, 0.55, 0.64, 44, 47),
    ("ChinaRare",         "China",   "Rare Earths",    83, 28, 3.5, 0.82, 0.88, 86, 89),
    ("USARare",           "USA",     "Rare Earths",    20, 22, 4.6, 0.22, 0.70, 18, 23),
    ("MalaysiaPlastic",   "Malaysia","Plastics",       33, 17, 4.2, 0.38, 0.77, 31, 35),
    ("SaudiChem",         "Saudi Arabia","Plastics",   48, 25, 3.8, 0.52, 0.72, 46, 50),
    ("NetherlandsChem",   "Netherlands","Plastics",    14, 13, 4.7, 0.18, 0.74, 12, 16),
    ("SingaporeTech",     "Singapore","Semiconductors",17, 14, 4.8, 0.20, 0.75, 15, 19),
    ("IsraelTech",        "Israel",  "Semiconductors", 42, 18, 4.3, 0.48, 0.74, 44, 46),
    ("IndonesiaNickel",   "Indonesia","Battery Metals", 42, 28, 3.8, 0.50, 0.70, 40, 44),
    ("PhilippineNickel",  "Philippines","Battery Metals",40,26,3.9,0.48,0.68,38,42),
    ("ZambiaCopper",      "Zambia",  "Battery Metals", 52, 32, 3.4, 0.60, 0.60, 50, 55),
    ("ChileLithium",      "Chile",   "Battery Metals", 34, 28, 4.0, 0.40, 0.66, 32, 36),
    ("MoroccoPhospho",    "Morocco", "Battery Metals", 38, 30, 3.9, 0.45, 0.64, 36, 40),
    ("NigeriaPlastic",    "Nigeria", "Plastics",       65, 35, 3.1, 0.72, 0.58, 64, 68),
    ("SouthAfricaMine",   "South Africa","Rare Earths",46,30,3.7,0.53,0.65,44,48),
    ("CzechAuto",         "Czech Republic","Steel",    22,15,4.5,0.26,0.76,20,24),
    ("HungarySemi",       "Hungary", "Semiconductors", 26, 16, 4.4, 0.30, 0.74, 24, 28),
    ("RomaniaMfg",        "Romania", "Steel",          32, 17, 4.1, 0.38, 0.72, 30, 34),
    ("TaiwanAdvanced",    "Taiwan",  "Semiconductors", 76, 17, 4.3, 0.73, 0.90, 79, 83),
    ("KoreaBattery",      "Korea",   "Battery Metals", 38, 19, 4.2, 0.44, 0.82, 36, 40),
    ("JapanBattery",      "Japan",   "Battery Metals", 21, 18, 4.6, 0.24, 0.78, 19, 22),
    ("FranceChem",        "France",  "Plastics",       16, 14, 4.6, 0.20, 0.73, 14, 17),
    ("SpainSteel",        "Spain",   "Steel",          20, 15, 4.5, 0.23, 0.75, 18, 21),
]

COLUMNS = [
    "name","country","material",
    "country_risk","lead_time","rating","price_volatility",
    "capacity_util","geo_score","risk_score"
]

def get_dataframe() -> pd.DataFrame:
    return pd.DataFrame(SUPPLIERS_DATA, columns=COLUMNS)

FEATURE_COLS = ["country_risk","lead_time","rating","price_volatility","capacity_util","geo_score"]
