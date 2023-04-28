"""
Gia Minh
Item list
04/20/2022
"""

ship_type = [

['next day air', "01"],
['overnight', "01"],
["ups overnight", "01"],
["ups next day air", "01"],
["2nd day", "02"],
["2nd day air", "02"],
["ups 2nd day air", "02"],
["ups 2nd day", "02"],
["ground", "03"],
["ups ground", "03"],
["priority", "usps_priority"],
["", ""],
]

def get_ship_type(input_type, oz):

    ship_code = ''
    # for x in input_type:
    for y in ship_type:
        if input_type in y:
            ship_code = y[1]

    if ship_code == "01" or ship_code == "02" or ship_code == "03" or ship_code == 'usps_priority':
        pass
    else:
        if oz >= 16:
            ship_code = "03"  # 93: UPS SurePost 1LB or greater
        elif oz < 16: #for usps
            ship_code = "usps_first"

    return ship_code


def get_ship_UPS(string):
    name =''
    if string == "01":
        name = 'UPS Overnight'
    elif string == '02':
        name = 'UPS 2nd Day Air'
    elif string == '03':
        name = 'UPS Ground'
    elif string == '93':
        name = 'UPS Sure Post'
    elif string == 'usps_first':
        name = 'USPS First Class'
    elif string == 'usps_priority':
        name = 'USPS Priority'
    return name


us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}