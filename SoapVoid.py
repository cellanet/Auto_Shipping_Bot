from tkinter import E
import xml.etree.ElementTree as ET
from zeep import Client, Settings
from zeep.exceptions import Fault
from pw import ups_api, ups_id, ups_pw


def UPS_Void(tracking):
    # Set Connection
    settings = Settings(strict=False, xml_huge_tree=True)
    client = Client('SCHEMA-WSDLs/Void.wsdl', settings=settings)

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

    # Create Void Shipment Dictionary
    voidShipmentDictionary = {
        'ShipmentIdentificationNumber': tracking
    }

    # Create Request Dictionary
    requestDictionary = {

        'RequestOption': 'Request Option'
    }

    # Try operation
    try:
        response= client.service.ProcessVoid(_soapheaders=headers, Request=requestDictionary, VoidShipment=voidShipmentDictionary)

        void = "Voided!"
        #print(response)

        return void

    except Fault as error:
        error = ET.tostring(error.detail)

        data = str(str(error).split("Description>")[1]).split("<")[0]
       #print(error)
        return data