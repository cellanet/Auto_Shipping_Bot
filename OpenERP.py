import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import NoSuchElementException
import datetime
from time import sleep
from pw import erp_id, erp_pw
from sendEmail import error_email_notify
from subprocess import CREATE_NO_WINDOW # This flag will only be available in windows
import chromedriver_autoinstaller


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def check_exists_by_xpath(xpath):
    try:
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return True
    except BaseException:
        return False


# ======================================== OPEN ERP ================================================
chromedriver_autoinstaller.install() # delete chromedriver first for it to work
# chrome_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
# chrome_service = ChromeService(chrome_path)
chrome_service = ChromeService("chromedriver.exe")

chrome_service.creationflags = CREATE_NO_WINDOW
driver = webdriver.Chrome(service=chrome_service)
driver.get("https://company-internal-webiste.com")

sleep(1.5)

#login here
input_id = driver.find_element(By.NAME, "login")
input_id.send_keys(erp_id)
input_id = driver.find_element(By.NAME, "password")
input_id.send_keys(erp_pw)
input_id.send_keys(Keys.RETURN)


# ========================= Find Ticket =====================
# click_customer_service = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Customer Service"))) <--- sample
def hand_off_and_log_note(string):
    # Hand off ticket
    handoff = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class= 'oe_button oe_form_button oe_highlight']")))

    sleep(0.25)
    handoff.click()

    # Hit cancel to go back to customer's ticket
    click_cancel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Cancel")))
    sleep(0.25)
    click_cancel.click()

    # click log a note
    sleep(1)
    lognote = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class= 'oe_compose_log']")))

    # paste value
    action = ActionChains(driver)
    action.click(lognote)
    action.pause(0.5)
    action.send_keys(string)
    action.perform()

    click_to_post = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class = 'oe_post']")))
    sleep(0.5)
    click_to_post.click()


def log_note_only(string):
    # click log a note
    lognote = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@class= 'oe_compose_log']")))
    sleep(1)
    # paste value
    action = ActionChains(driver)
    action.click(lognote)
    action.pause(1)
    action.send_keys(string)
    action.perform()
    click_to_post = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@class = 'oe_post']")))
    sleep(0.5)
    click_to_post.click()


def post_message(string):
    # click log a note
    lognote = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class= 'oe_compose_post']")))

    # paste value
    action = ActionChains(driver)
    action.click(lognote)
    action.pause(1)
    action.send_keys(string)
    action.perform()

    click_to_post = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class = 'oe_post']")))
    sleep(0.5)
    click_to_post.click()


def hand_off_send_message(string):
    # Hand off ticket
    handoff = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class= 'oe_button oe_form_button oe_highlight']")))
    sleep(0.7)
    handoff.click()

    # Hit cancel to go back to customer's ticket
    sleep(1)
    click_cancel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Cancel")))
    click_cancel.click()

    # click send message
    sleep(2)
    lognote = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@class= 'oe_compose_post']")))

    sleep(1)
    # paste value
    action = ActionChains(driver)
    action.click(lognote)
    action.pause(1)
    action.send_keys(string)
    action.perform()

    sleep(0.5)
    click_to_post = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class = 'oe_post']")))
    click_to_post.click()


def cancel(string):
    # click send message
    sleep(0.5)
    lognote = WebDriverWait(driver, 3).until(
        EC.presence_of_element_located((By.XPATH, "//a[@class= 'oe_compose_post']")))
    sleep(0.8)
    # paste value
    action = ActionChains(driver)
    action.click(lognote)
    action.pause(1)
    action.send_keys(string)
    action.perform()

    #hit to post msg
    sleep(0.5)
    click_to_post = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class = 'oe_post']")))
    click_to_post.click()

    sleep(2)
    cancel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[@class= 'oe_button oe_form_button oe_highlight fixed_width_button']")))
    cancel.click()
    return -1

def scan_for_info():
    try:
        # CLICK CUSTOMER SERVICE
        driver.get('https://company-internal-webiste.com/?ts=#page=0&limit=80&view_type=list&model=customer_service.ticket&menu_id=510&action=634')
        #click_customer_service = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Customer Service")))
        #sleep(0.25)
        #click_customer_service.click()

        # ***************************************************************************************************************************************
        # CLICK MY TICKET
        my_ticket = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//span[@class='oe_menu_text' and (contains(text(),'My Tickets'))]")))
        sleep(0.5)
        my_ticket.click()
        # ***************************************************************************************************************************************
        # CLICK FIRST TICKET
        sleep(1)
        check_if_ticket_exists = check_exists_by_xpath("//td[@title='Number of customer service ticket']")

        if check_if_ticket_exists:
            found = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//td[@title='Number of customer service ticket']")))
            sleep(1)
            found.click()

            # if work flow  == me:
            current_owner = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='oe_form_field oe_form_field_selection']"))).text
            if current_owner == 'IT - Test':
                # GET CUSTOMER INFO
                info = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//span[@class='oe_form_text_content']"))).text
                customer_info = info.splitlines()

                # get customer phone + ticket number
                contact_info = driver.find_elements(By.XPATH, "//span[@class='oe_form_char_content']")
                ticket_status = contact_info[1].text
                ticket_number = contact_info[4].text
                print("Ticket number: %s" % ticket_number)
                customer_phone = contact_info[6].text
                customer_email = contact_info[9].text

                if len(customer_info) < 5:
                    raise Exception("ERP-0: Missing customer's info. Please double check name, address, city, state, zip code.\n\nPlease make a new ticket.\nThanks.\n\nLogged by bot")

                # GET ITEM TO SHIP
                service_issue = driver.find_elements(By.XPATH, "//span[@class='oe_form_text_content']")
                service_issue0 = service_issue[1].text  # [1] because //span[@class='oe_form_text_content']")[0] = Cutomer's default address on ERP
                service_issue = service_issue0.splitlines()[0]  # get rid of every after "enter key"
                # service_issue = service_issue[0]

                # NAME
                customer_name = 'N/A name'
                customer_street = "N/A street"
                customer_city = 'N/A city'
                customer_state = "N/A state"
                customer_zip = "N/A zip"

                print("\n\n ===== New Transaction =====\n")

                customer_name = customer_info[2]
                print(customer_name)
                customer_street = customer_info[3]
                print(customer_street)
                # CITY
                # print(f"name {customer_name}, street {customer_street} city {customer_info[4]}")

                if ',' in customer_info[4]:
                    split_city = customer_info[4].split(',')
                else:
                    raise Exception("ERP-1: Error in CITY and STATE. Please double check if the address was put into corresponding boxes.\n\nPlease cancel this ticket and make a new one.\nThanks.\n\nLogged by bot")

                customer_city = split_city[0]

                print(split_city)
                if len(split_city) == 2:
                    split_state = re.search(r"(\D{1,} )(.*)", split_city[1])
                    customer_state = str(split_state.group(1)).strip()
                    customer_zip = split_state.group(2)

                    print(f"State: {customer_state}.\nZip: {customer_zip}.")
                else:
                    raise Exception("ERP-2: Missing City or State. Please double check if address was put in corresponding boxes.\n\nPlease create new ticket.\nThank you.\n\nLogged by bot")

                customer_country = "n/a country"
                if len(customer_info) > 5:
                    #get country name, strip and change to lower case
                    customer_country = customer_info[5].lower().strip()

                    # strip space between character in zipcode (for canada and ?)
                    customer_zip = customer_zip.replace(" ","")

                    # for international only, if there is no phone number, then use ULO phone number
                    if not has_numbers(customer_phone):
                        customer_phone = "323-316-4514"
                    print(f"Country: {customer_country}.")
                else:
                    customer_zip = str(customer_zip)[:5]
                    if not customer_zip.isdigit():
                        raise Exception(
                            "ERP-3: Missing/invalid State/Zip Code OR this is an international address if so please add country name.\n\nPlease double check and make a new ticket.\n\nLogged by bot.")

                # SPLIT ALL ITEM INSIDE USING +/-
                ship_type = 'empty'
                if ":" in service_issue:
                    ship_type = str(service_issue.split(":")[0]).lower()
                    items = str(service_issue.split(":")[1])
                    items = items.split("+")
                else:
                    items = service_issue.split("+")

                error = 0

                return customer_name, customer_street, customer_city, customer_state, customer_zip, customer_phone, ticket_number, ship_type, items, service_issue, customer_info, error, customer_country, customer_email
            else:
                print("I'm not the ticket owner")
        elif check_if_ticket_exists == False:
            # complete cycle = 295 seconds
            for i in range(287, 0, -1): # range=287 for cycle = 295
                sleep(1)
                if i%10 == 0:
                    print(i)
                if i <= 15:
                    print(i)

    except BaseException as e:

        print("\nError from OpenERP\n")
        if str(e) == 'list index out of range':
            e = "Please check customer's info"

        sleep(1)
        action = ActionChains(driver)
        action.key_up(Keys.PAGE_DOWN)
        action.perform()
        sleep(0.5)
        error = cancel(str(e))

        sleep(0.5)
        date = f"{datetime.date.today()} - {datetime.datetime.now().hour}:{datetime.datetime.now().minute}"
        ticket = f"Ticket: {ticket_number}.\n\nName: {customer_name}\n{customer_street}\n{customer_city}, {customer_state} {customer_zip}."
        raw_data = f"\n\nRaw data: {customer_info}.\nItem: {service_issue}.\nError: {e}\n=====================\n\n"

        error_log = f"{date}.\n{ticket}\n{raw_data}"

        file = open('error.txt', 'a')
        file.write(error_log)
        file.close()

        # send email to Minh
        error_email_notify(error_log)
        print("\nLogged and emailed errors.")
            # print(str(e))




