from OpenERP import hand_off_and_log_note, log_note_only, scan_for_info, cancel
from time import sleep
import datetime

from ZPL_Label_Convert import printNoti
from UPS import UPS_print, UPS_return, UPS_Rate
from USPS import USPS, USPS_Return, USPS_international
from itemList import get_weight, get_quantity
from ShipFilter import get_ship_UPS, get_ship_type, us_state_to_abbrev
import math
from zeep.exceptions import Fault
from CustomerInfo import insert_data
from sendEmail import error_email_notify

# click_customer_service = driver.find_element(By.LINK_TEXT, "Customer Service")    <--- sample

def UPS_API():
    try:
        error = -1
        try:
            customer_name, customer_street, customer_city, customer_state, customer_zip, customer_phone, ticket_number, ship_type, items, service_issue, customer_info, error, customer_country, customer_email = scan_for_info()
        except:
            raise BaseException('No new ticket')

        us = ['N/A country', 'US', 'U.S', 'United States', 'USA']
        us = [x.lower() for x in us]

        if len(customer_name) >= 23:
            hand_off_and_log_note("Customer's name too long, anh Toan Please Ship this.")
        else:
            if len(customer_state) == 2:
                customer_state = customer_state.upper()
            elif len(customer_state) > 2 and customer_country in us:
                customer_state = str(us_state_to_abbrev[customer_state.strip()]).upper()

            # CHECK POINT FOR PUERTO RICO
            if customer_state == 'PR':
                customer_country = 'Puerto Rico'

            # Get item(s) from raw input string
            items = list((map(lambda x: x.lower(), items)))  # CONVERT TO LOWER CASE
            oz = get_weight(items)
            print(items)

            # GET QUANTITY
            oz += get_quantity(items)  # Only count if quantity is > 1
            if oz == 0:
                error = 0
                raise BaseException("SHIP-1: Missing/Invalid item(s) or New Item Detected. Please double check item's name and spelling.")
            lbs = math.ceil(oz / 16)
            print("oz: " + str(oz))
            print("lbs: " + str(lbs))

            # GET SHIP TYPE - NEXT DAY AIR / 2ND DAY AIR
            # ship_type = service_issue.split(":")
            # ship_type = list((map(lambda x: x.lower(), ship_type)))
            if ship_type != 'empty':
                print(ship_type)
            ship_code = get_ship_type(ship_type, oz)
            print("Ship code: " + ship_code)

            tracking = "N/A"
            rsl_tracking = "N/A"

            unit_lb = 'LBS'
            unit_oz = 'OZS'

            # DOMESTIC SHIPPING
            if customer_country in us:
                customer_country = 'US'

                residental = UPS_Rate(customer_name, customer_street, customer_city, customer_state, customer_zip)
                print(f"\n\nResidential: {residental}.")
                if residental:
                    if (ship_code == "03" and ship_type != 'ground') and oz <= 32:
                        ship_code = "93"

                ship_name = get_ship_UPS(ship_code)

                # Noti for nextdayair, 2nddayair
                printNoti(ship_name)

                # ====== GENERATE SHIPPING LABELS HERE ======
                # For UPS
                if ship_code == "01" or ship_code == "02" or ship_code == "03" or ship_code == "93":
                    # if customer_state == 'PR':
                    #     customer_country = 'PR'
                    tracking = UPS_print(customer_name, customer_street, customer_city, customer_state, customer_zip,
                                         customer_phone, lbs, ship_code, ticket_number, customer_country)
                # For USPS
                elif ship_code == "usps_first" or ship_code == 'usps_priority':
                    tracking = USPS(customer_name, customer_street, customer_city, customer_state, customer_zip, oz,
                                    ticket_number, ship_code, customer_country)
                # ERROR
                elif ship_code == "-1":
                    raise BaseException("SHIP-2: Unknown or can't determine Shipping Type.")

                # return label
                if 'rsl' in service_issue.lower():
                    if oz < 16:
                        # Use USPS
                        rsl_tracking = USPS_Return(customer_name, customer_street, customer_city, customer_state,
                                                   customer_zip, oz, ticket_number, customer_country, "usps_first")
                    else:
                        # Use UPS
                        rsl_tracking = UPS_return(customer_name, customer_street, customer_city, customer_state,
                                                  customer_zip, customer_phone, lbs, ticket_number, customer_country)

            # To Canada and Puerto Rico, no matter the weight, always use USPS for Canada
            elif customer_country == 'canada' or customer_country == 'Puerto Rico':
                # check weight to assign value
                if oz < 9:
                    value = 9.95
                else:
                    value = 195

                if customer_country == 'canada':
                    ship_name = 'USPS First Class International'
                    tracking = USPS_international(customer_name, customer_street, customer_city, customer_state,
                                                  customer_zip, customer_phone, customer_country, oz, ticket_number, value)
                    residental = 'False'

                else:
                    customer_country = 'US'
                    if oz < 16:
                        ship_code = 'usps_first'
                        ship_name = 'USPS First Class'
                    else:
                        ship_code = 'usps_priority'
                        ship_name = 'USPS Priority'
                    residental = 'False'

                    # Ship label
                    tracking = USPS(customer_name, customer_street, customer_city, customer_state, customer_zip, oz,
                                    ticket_number, ship_code, customer_country)
                    # return label
                    if 'rsl' in service_issue.lower():
                        if oz < 16:
                            ship_code = 'usps_first'
                        else:
                            ship_code = 'usps_priority'

                        # RSL Label
                        rsl_tracking = USPS_Return(customer_name, customer_street, customer_city, customer_state,
                                                   customer_zip, oz, ticket_number, customer_country, ship_code)

            # international shipping here, below 9oz will ship with USPS, else ship with DHL
            else:
                if oz < 9:
                    value = 9.95
                    ship_name = 'USPS First Class International'
                else:
                    value = 195
                    ship_name = 'DHL World Express'

                tracking = USPS_international(customer_name, customer_street, customer_city, customer_state, customer_zip,
                                       customer_phone, customer_country, oz, ticket_number, value)
                residental = 'False'

            # Get tracking info here
            tracking_numbers = f"Tracking number:\n{tracking}.\nRSL: {rsl_tracking}.\nShip by: {ship_name}.\n\nItem(s): {service_issue}.\nResidential: {residental}.\n\nWeight: {oz}oz or {lbs}lb.\n\nShip to:\n{customer_name}\n{customer_street}\n{customer_city}, {customer_state} {customer_zip}\n{customer_country}\n\nPhone number: {customer_phone}.\nEmail: {customer_email}.\n\nLogged by bot."

            # LOG TICKET HERE
            if tracking != "N/A" and 'error' not in tracking:
                # log_note_only(tracking_numbers)
                #Log everything here to ERP
                hand_off_and_log_note(tracking_numbers)
                print(tracking_numbers)
            elif 'Recipient address invalid' in tracking:
                hand_off_and_log_note(f'SHIP-3: Unusual address. Anh Toan please ship.\n\nOriginal error from USPS/UPS/Fedex: {tracking}')
            # elif tracking == "N/A":
            #     raise BaseException("SHIP-4: No label generated. Either UPS/USPS server is down or something is wrong with this ticket.\nPlease tag Minh here.")
            elif 'error' in tracking and 'Recipient address invalid' not in tracking:#or ('error' in rsl_tracking):
                raise BaseException(f"SHIP-4: {tracking}")
            # still need to catch error from UPS and Fedex to complete this block

            sleep(1)
            printNoti(ship_name)

            if 'USPS' in ship_name:
                carrier = 'usps'
            elif 'DHL' in ship_name:
                carrier = 'dhl'
            elif 'UPS' in ship_name:
                carrier = 'ups'

            delivered = None
            deliveryDate = None
            sendEmailDate = None
            chargeEmail = None

            insert_data(ticket_number, customer_email, carrier, tracking, delivered, deliveryDate, sendEmailDate,
                        chargeEmail)

    except BaseException as e:  # Exception as e

        if str(e) != 'No new ticket':
            print("\nFrom SoapShip\n")
            if e == 'list index out of range':
                e = "Please check customer's info"
            error_note = "\n\nERROR: " + str(e) + "\n\n\nIf you think this ticket is correct please tag Minh here\n\nOtherwise please check Customer's address and Service Issue box and create new ticket, this ticket will be cancelled.\nThank you\n\nLogged by bot."
            sleep(0.5)

            if error == -1:
                log_note_only(error_note)
            elif error == 0:
                cancel(error_note)

            sleep(0.5)
            date = f"{datetime.date.today()} - {datetime.datetime.now().hour}:{datetime.datetime.now().minute}"
            ticket = f"Ticket: {ticket_number}.\n\nName: {customer_name}\n{customer_street}\n{customer_city}, {customer_state} {customer_zip}."
            raw_data = f"\n\nRaw data: {customer_info}.\nItem: {service_issue}.\nError: {e}\n=====================\n\n"

            error_log = f"{date}.\n{ticket}\n{raw_data}"

            file = open('error.txt', 'a')
            file.write(error_log)
            file.close()

            #send email to Minh
            error_email_notify(error_log)
            print("\nLogged errors.")
        else:
            print('No new ticket. Refreshing browser now.')