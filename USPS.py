import shippo
from ZPL_Label_Convert import USPS_convert_zpl, USPS_RSL_convert_zpl, USPS_international_convert_zpl
from zeep.exceptions import Fault
from OpenERP import cancel
from pw import shippo_api

shippo.config.api_key = shippo_api

def USPS(customer_name, customer_street, customer_city, customer_state, customer_zip, oz, ticket_number, service, country):
    address_from = {
        "name": "Ultralight Optics INC",
        "street1": "7200 Hazard Ave",
        "city": "Westminster",
        "state": "CA",
        "zip": "92683",
        "country": "US"
    }

    address_to = {
        "name": customer_name,
        "company": ticket_number,
        "street1": customer_street,
        "city": customer_city,
        "state": customer_state,
        "zip": customer_zip,
        "country": country
    }

    parcel = {
        "length": "7",
        "width": "5",
        "height": "4",
        "distance_unit": "in",
        "weight": oz,
        "mass_unit": "oz"
    }

    shipment = {
        "address_from": address_from,
        "address_to": address_to,
        "parcels": [parcel],
        # async = False
    }

    try:
        transaction = shippo.Transaction.create(
            shipment=shipment,
            carrier_account="27ff246064124d96822f330017bd9e73",
            servicelevel_token= service
        )

        print(f"\nNew transaction: \n\n{transaction.status}")

        label ="n/a"

        if transaction.status == "SUCCESS":
            label = transaction.label_url
        else:
            for message in transaction.messages:
                raise BaseException("\n-This error note is from USPS: \n\n%s" % message['text'])

        if label != 'n/a':
            USPS_convert_zpl(label)
        else:
            raise BaseException("USPS-1: Label's URL incorrect.")

        return transaction.tracking_number

    except BaseException as e:
        return str(e)

def USPS_Return(customer_name, customer_street, customer_city, customer_state, customer_zip, oz, ticket_number, country, ship_code):
    address_from = {
        "name": "Ultralight Optics INC",
        "street1": "7200 Hazard Ave",
        "city": "Westminster",
        "state": "CA",
        "zip": "92683",
        "country": "US"
    }

    address_to = {
        "name": customer_name,
        "company": ticket_number,
        "street1": customer_street,
        "city": customer_city,
        "state": customer_state,
        "zip": customer_zip,
        "country": country
    }

    parcel = {
        "length": "7",
        "width": "5",
        "height": "4",
        "distance_unit": "in",
        "weight": oz,
        "mass_unit": "oz"
    }

    shipment = {
        "address_from": address_from,
        "address_to": address_to,
        "parcels": [parcel],
        "extra": {'is_return': True},
    # async = False
    }

    try:
        transaction = shippo.Transaction.create(
            shipment=shipment,
            carrier_account="27ff246064124d96822f330017bd9e73",
            servicelevel_token= ship_code
        )

        print(f"\nNew transaction: \n\n{transaction.status}")

        label ="n/a"

        if transaction.status == "SUCCESS":
            label = transaction.label_url
        else:
            for message in transaction.messages:
                raise BaseException("\n-This error note is from USPS return: \n\n%s" % message['text'])

        if label != 'n/a':
            USPS_RSL_convert_zpl(label)
        else:
            raise BaseException("USPS RSL-2: Label's URL incorrect.")

        return transaction.tracking_number

    except BaseException as e:
        return str(e)


def USPS_international(customer_name, customer_street, customer_city, customer_state, customer_zip, customer_phone, customer_country, oz, ticket_number, value):
    address_from = {
        "name": "Ultralight Optics INC",
        "street1": "7200 Hazard Ave",
        "city": "Westminster",
        "state": "CA",
        "zip": "92683",
        'phone': '(323) 316-4514',
        "country": "US"
    }

    address_to = {
        "name": customer_name,
        "company": ticket_number,
        "street1": customer_street,
        "city": customer_city,
        "state": customer_state,
        "zip": customer_zip,
        "phone": customer_phone,
        "country": customer_country
    }

    parcel = {
        "length": "7",
        "width": "5",
        "height": "4",
        "distance_unit": "in",
        "weight": oz,
        "mass_unit": "oz"
    }

    customs_item = {
        "description": "small LED Unit",
        "quantity": '1',
        "net_weight": oz,
        "mass_unit": "oz",
        "value_amount": value,
        "value_currency": "USD",
        "origin_country": "US",
        "tariff_number": "",
    }

    customs_declaration = {
        'contents_type': 'RETURN_MERCHANDISE',
        'contents_explanation': 'Warranty Replacement',
        'non_delivery_option': 'RETURN',
        'certify': True,
        'certify_signer': 'Vivian',
        'incoterm': 'DDP',
        'items': [customs_item]
    }

    shipment = {
        "address_from": address_from,
        "address_to": address_to,
        "parcels": [parcel],
        'customs_declaration': customs_declaration,
        # "extra": {
        #     "bypass_address_validation": True
        # }
    }

    try:

        # # ef58d81133b54130b9290237c17e2b21 dhl || usps 27ff246064124d96822f330017bd9e73
        # carrier_account = "27ff246064124d96822f330017bd9e73",
        # # 'dhl_express_worldwide', usps_first_class_package_international_service
        # servicelevel_token = "usps_first_class_package_international_service"

        # print(shippo.CarrierAccount.all(carrier="usps")) #dhl_express
        if customer_country == 'canada' or customer_country == 'US':
            transaction = shippo.Transaction.create(
                shipment=shipment,
                # ef58d81133b54130b9290237c17e2b21 dhl || usps 27ff246064124d96822f330017bd9e73
                carrier_account="27ff246064124d96822f330017bd9e73",
                # 'dhl_express_worldwide', usps_first_class_package_international_service
                servicelevel_token="usps_first_class_package_international_service"
            )
        else:
            if oz < 9:
                transaction = shippo.Transaction.create(
                    shipment=shipment,
                    # for USPS international
                    carrier_account="27ff246064124d96822f330017bd9e73",
                    # token
                    servicelevel_token= "usps_first_class_package_international_service"
                )
            else:
                transaction = shippo.Transaction.create(
                    shipment=shipment,
                    # for dhl express worldwide
                    carrier_account="ef58d81133b54130b9290237c17e2b21",
                    # token
                    servicelevel_token="dhl_express_worldwide"
                )

        print(f"\nNew transaction: \n\n{transaction.status}")

        label = "n/a"

        if transaction.status == "SUCCESS":
            label = transaction.label_url
        else:
            for message in transaction.messages:
                cancel("\n-This error note is from USPS International: \n\n%s" % message['text'])

        if label != 'n/a':
            USPS_international_convert_zpl(label)
        else:
            raise Exception("USPS-International: Label's URL incorrect.")

        return transaction.tracking_number

    except Fault as e:
        print(str(e))