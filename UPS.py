import base64
from ZPL_Label_Convert import convert_zpl, convert_zpl_RSL
import xml.etree.ElementTree as ET
from zeep import Client, Settings
from zeep.exceptions import Fault
from zeep import helpers
from OpenERP import cancel
from SoapReship import UPS_reprint_label
from pw import ups_id, ups_pw, ups_api, ups_tax

def UPS_print(name, street, city, state, zip, phone, weight, type, ticket, country):

    # Set Connection
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client('SCHEMA-WSDLs/Ship.wsdl', settings=settings)

    # Set SOAP Headers
    headers = {

        'UPSSecurity': {
            'UsernameToken': {
                'Username': ups_id,
                'Password': ups_pw
            },

            'ServiceAccessToken': {
                'AccessLicenseNumber': ups_api
            }

        }
    }

    # Create request dictionary
    requestDictionary = {

        "RequestOption": "nonvalidate", #nonvalidate or validate
        "TransactionReference": {
            "CustomerContext": "ULO Bot"
        }
    }

    # Create Ship request dictionary
    shipmentRequestDictionary = {

        #"Description": "Ship WS test",
        "Package": {
            # "Description": ticket,
            "Dimensions": {
                "Height": "4",
                "Length": "12",
                "UnitOfMeasurement": {
                    "Code": "IN",
                    "Description": "Inches"
                },
                "Width": "7"
            },
            "PackageWeight": {
                "UnitOfMeasurement": {
                    "Code": 'LBS', # LBS, OZS unit
                    "Description": "Pounds"
                },
                "Weight": weight # weight
            },
            "ReferenceNumber": {
            "Value": ticket         # <--- TICKET NUMBER GO HERE
            },
            "Packaging": {
                "Code": "02",
                "Description": "Customer Supplied Package"
            }
        },
        "PaymentInformation": {
            "ShipmentCharge": {
                "BillShipper": {
                    "AccountNumber": "7196FE"
                },
                "Type": "01"
            }
        },
        # 92: UPS SurePost Less than 1LB
        # 93: UPS SurePost 1LB or greater
        # 94: UPS SurePost BPM
        # 95: UPS SurePost Media Mail
        "Service": {
            "Code": type, # type
            "Description": "Ground"
        },
        # "USPSEndorsement": "5",
        #"PackageID": "ticketnumber",

        "ShipFrom": {
            "Address": {
                "AddressLine": "7200 hazard ave",
                "City": "westminster",
                "CountryCode": "US",
                "PostalCode": "92683",
                "StateProvinceCode": "CA"
            },
            "AttentionName": "",
            "FaxNumber": "",
            "Name": "ULO",
            "Phone": {
                "Number": "323-316-4514"
            }
        },
        "ShipTo": {
            "Address": {
                "AddressLine": street,
                "City": city,
                "CountryCode": country,
                "PostalCode": zip,
                "StateProvinceCode": state,
            },
            "AttentionName": "",
            "Name": f"{name} - {ticket}",
            "Phone": {
                "Number": "323-316-4514"
            }
        },
        "Shipper": {
            "Address": {
                "AddressLine": "7200 hazard ave",
                "City": "Westminster",
                "CountryCode": "US",
                "PostalCode": "92683",
                "StateProvinceCode": "CA"
            },
            "AttentionName": "",
            "FaxNumber": "",
            "Name": "Ultralight Optics Inc",
            "Phone": {
                "Extension": "",
                "Number": "323-316-4514"
            },
            "ShipperNumber": "7196FE",
            "TaxIdentificationNumber": ups_tax
        }

    }
    # Create label specification dictionary
    labelSepcificationDictionary = {
        "HTTPUserAgent": "Mozilla/4.5",
        "LabelImageFormat": {
            "Code": "ZPL",
            "Description": "ZPL"
        },
        "LabelStockSize": {
            "Height": "6",
            "Width": "4"
        }
    }
    # Try operation
    try:
        response = client.service.ProcessShipment(_soapheaders=headers,Request=requestDictionary,Shipment=shipmentRequestDictionary, LabelSpecification=labelSepcificationDictionary)

        # print(response)

        data = helpers.serialize_object(response, dict)
        data_to_list = str(data).strip()
        data_to_list = str(data).split("'")

        base64_code = '-1'
        count = 0

        check_label = str(str(data).split("'ShippingLabel':")[1]).split(",")[0].strip()
        if check_label == 'None':
            tracking = str(str(data).split("'TrackingNumber': '")[1]).split("'")[0]
            UPS_reprint_label(tracking)

        else:
            base64_code = str(str(data).split("'GraphicImage': '")[1]).split("'")[0]
            # print(f"base: {base64_code}")
            ups_label = base64.b64decode(base64_code)
            convert_zpl(ups_label)

            for x in data_to_list:
                if '1Z7196' in x:
                    tracking = x

        return tracking

    except Fault as error:
        detail = str(ET.tostring(error.detail))
        detail = detail.split("Description")
        detail = detail[1].replace("</ns0:", "")

        msg = f"From UPS's Server:\n{detail}."
        cancel(msg)


def UPS_return(name, street, city, state, zip, phone, weight, ticket, country):
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client('SCHEMA-WSDLs/Ship.wsdl', settings=settings)
    headers = {
        'UPSSecurity': {
            'UsernameToken': {
                'Username': ups_id,
                'Password': ups_pw
            },
            'ServiceAccessToken': {
                'AccessLicenseNumber': ups_api
            }
        }
    }
    # Create request dictionary
    requestDictionary = {

        "RequestOption": "validate",
        "TransactionReference": {
            "CustomerContext": "Replacement"
        }
    }
    # Create Ship request dictionary
    shipmentRequestDictionary = {

        "Description": "Warranty item",
        "ReturnService": {
            "Code": "9"
        },
        "Package": {
            "Description": ticket,
            "Dimensions": {
                "Height": "7",
                "Length": "15",
                "UnitOfMeasurement": {
                    "Code": "IN",
                    "Description": "Inches"
                },
                "Width": "12"
            },
            "PackageWeight": {
                "UnitOfMeasurement": {
                    "Code": "LBS",
                    "Description": "Pounds"
                },
                "Weight": weight
            },
            "ReferenceNumber": {
                "Value": ticket
            },
            "Packaging": {
                "Code": "02",
                "Description": "Customer Supplied Package"
            }
        },
        "PaymentInformation": {
            "ShipmentCharge": {
                "BillShipper": {
                    "AccountNumber": "7196FE"
                },
                "Type": "01"
            }
        },
        "Service": {
            "Code": "03",
            "Description": "GROUND"
        },
        "ShipFrom": {
            "Address": {
                "AddressLine": street,
                "City": city,
                "CountryCode": country,
                "PostalCode": zip,
                "StateProvinceCode": state,
            },
            "AttentionName": "",
            "FaxNumber": "",
            "Name": f"{name} - {ticket}",
            # "Phone": {
            #     "Number": phone
            # }
        },
        "ShipTo": {
            "Address": {
                "AddressLine": "7200 hazard ave",  #
                "City": "westminster",  #
                "CountryCode": "US",
                "PostalCode": "92683",  #
                "StateProvinceCode": "CA"  #
            },
            "AttentionName": "",
            "Name": "Utralight Optics",  #
            "Phone": {
                "Number": "323-316-4514"  #
            }
        },
        "Shipper": {
            "Address": {
                "AddressLine": "7200 hazard ave",
                "City": "Westminster",
                "CountryCode": "US",
                "PostalCode": "92683",
                "StateProvinceCode": "CA"
            },
            "AttentionName": "",
            "FaxNumber": "",
            "Name": "Ultralight Optics Inc",
            "Phone": {
                "Extension": "1",
                "Number": "323-316-4514"
            },
            "ShipperNumber": "7196FE",
            "TaxIdentificationNumber": ups_tax
        }
    }
    # Create label specification dictionary
    labelSepcificationDictionary = {
        "HTTPUserAgent": "Mozilla/4.5",
        "LabelImageFormat": {
            "Code": "ZPL",
            "Description": "ZPL"
        },
        "LabelStockSize": {
            "Height": "6",
            "Width": "4"
        }
}

    # Try operation
    try:
        response = client.service.ProcessShipment(_soapheaders=headers, Request=requestDictionary,
                                                Shipment=shipmentRequestDictionary,
                                                LabelSpecification=labelSepcificationDictionary)
        # print(response)

        data = helpers.serialize_object(response, dict)
        data_to_list = str(data).strip()
        data_to_list = str(data).split(',')
        data_to_list = str(data).split('{')
        data_to_list = str(data).split("'")

        base64_code = '-1'
        count = 0
        tracking = '-2'

        base64_code = str(str(data).split("'GraphicImage': '")[1]).split("'")[0]
        # print(f"base: {base64_code}")

        ups_label = base64.b64decode(base64_code)
        convert_zpl_RSL(ups_label)

        for x in data_to_list:
            if '1Z7196' in x:
                tracking = x

        return tracking

    except Fault as error:
        detail = str(ET.tostring(error.detail))
        detail = detail.split("Description")
        detail = detail[1].replace("</ns0:", "")

        msg = f"From UPS's (Return) Server:\n{detail}."
        cancel(msg)


def UPS_Rate(name, address, city, state, zipcode):
    # Set Connection
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client('SCHEMA-WSDLs/RateWS.wsdl', settings=settings)

    # Set SOAP headers
    headers = {
        'UPSSecurity': {
            'UsernameToken': {
                'Username': ups_id,
                'Password': ups_pw
            },
            'ServiceAccessToken': {
                'AccessLicenseNumber': ups_api
            }
        }
    }
    # Create request dictionary
    requestDictionary = {
        "RequestOption": "Rate",
        "TransactionReference": {
            "CustomerContext": "Check Residental Address"
        }
    }
    # Create rate request dictionary
    rateRequestDictionary = {
        "Package": {
            "Dimensions": {
                "Height": "10",
                "Length": "5",
                "UnitOfMeasurement": {
                    "Code": "IN",
                    "Description": "inches"
                },
                "Width": "4"
            },
            "PackageWeight": {
                "UnitOfMeasurement": {
                    "Code": "Lbs",
                    "Description": "pounds"
                },
                "Weight": "1"
            },
            "PackagingType": {
                "Code": "02",
                "Description": "Rate"
            }
        },
        "Service": {
            "Code": "03",
            "Description": "Service Code"
        },
        "ShipFrom": {
            "Address": {
                "AddressLine": [
                    "7200 hazard ave",
                ],
                "City": "westminster",
                "PostalCode": "92683",
                "StateProvinceCode": "CA",
                "CountryCode": "US"

            },
            "Name": "ULO"
        },
        "ShipTo": {
            "Address": {
                "AddressLine": address,
                "City": city,
                "PostalCode": zipcode,
                "StateProvinceCode": state,
                "CountryCode": "US"

            },
            "Name": name
        },
        "Shipper": {
            "Address": {
                "AddressLine": [
                    "7200 hazard ave",
                ],
                "City": "westminster",
                "PostalCode": "92683",
                "StateProvinceCode": "CA",
                "CountryCode": "US"
            },
            "Name": "ULO",
            "ShipperNumber": "7196FE"
        }
    }
    # Try operation
    try:
        response = client.service.ProcessRate(_soapheaders=headers, Request=requestDictionary,                                         Shipment=rateRequestDictionary)

        data = str(helpers.serialize_object(response, dict)).split("'")
        #print(data)

        residential = False

        for x in data:
            if 'Residential' in x:
                residential = True

        return residential

    except Fault as error:
        print(ET.tostring(error.detail))