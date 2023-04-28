import re

"""
Gia Minh
Item list
3/25/2022

ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE

Please follow this format: [
                            ["item1", weight_of_item1],
                            ["item2", weight_of_item2]
                            ]


            example:       [
                             ["hf battery", 12],
                             ["elite", 4]
                           ]

ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE - ALL LOWER CASE

"""

# ================================================
def getItemList():
    item_list = {}

    file = open("item_list.txt", 'r')
    line = file.readlines()

    for x in line:
        (key, val) = x.split(",")
        item_list[key] = float(str(str(val).strip("\n")).strip())

    # x = '3rd gen omega battery'

    # if x in item_list:
    #     print(item_list[x])
    # ===================

    attachments = []

    file2 = open("attachment.txt", 'r')
    line2 = file2.readlines()

    for x in line2:
        attachments.append(x.strip('\n').strip())

    return item_list, attachments

# ================================================

"""
show shipping rate ? 
show shipping type: overnight, 2nd day ?
show item shipped ?
show weight ?
show shipto address ?
Layout void/reprint ?
Work flow for URGEN ticket?

State must be format into 2 character code => california = CA

                    / QA Attachment or Quick Attach Attachment /
how about this : 2x ULO Quick Attach for light + screws + nuts + washers = CS00391508
                	ULO QA  = 391472
                	WORKING EXAMPLE : ULO TTL Attachment = CS00391467

Special case: 3rd Gen Battery + DFV Steam + Crews goggles with attachment = CS00391398 || comp filter = CS00391372
                                screws, screws and nuts, crew goggles ???

Xtine: backing, 2x Perioptix Adivista = CS00391704
"""


def get_weight(input_string):

    item_list, attachments = getItemList()
    count0 = 0
    count1 = 0

    attach = str(input_string).split(" ")

    for x in input_string:
        x = x.strip()
        for z in attachments:
            if z in x:
                count0 = 4
                print(f"Items = {x.strip()}. Attachment's weight = {count0}")

        if ("visor" in x and len(x) > 5) and 'attachment' not in x:
            x = x.split(" ")[1]
        if x in item_list:
            count1+= item_list[x]
            print(f"Items = {x.strip()}. Item's weight = {count1}")
    if count1 >= 4 :
        count = count1
    else:
        count = count0 + count1
    return count


def get_quantity(list):
    weight = 0
    item_quantity = []
    quantity = ''
    item = ''
    item_list, attachments = getItemList()

    for i, x in enumerate(list):
        # print(f'{x=}')
        xnumber = re.compile(r'\b\d{1,}[x]')
        result = xnumber.search(x)
        if result:
            search = re.search(r'(\b\d{1,})(x)(.*)', x, re.DOTALL)
            quantity = search.group(1)
            item = search.group(3).strip()
            if int(quantity) > 1 and 'attachment' not in item:
                if "omega" in item and ("battery" in item or "batteries" in item):
                    item = "multiple battery"
                for y in range(int(quantity)):
                    item_quantity.append(item)
                weight += get_weight(item_quantity)
            elif int(quantity) == 1 and item not in attachments:
                item_quantity.append(item)
                weight = get_weight(item_quantity)

    return weight