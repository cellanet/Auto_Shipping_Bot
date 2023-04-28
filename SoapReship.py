import xml.etree.ElementTree as ET
from zeep import Client, Settings
from zeep.exceptions import Fault
from ZPL_Label_Convert import convert_zpl_Reprint
from zeep import helpers
import base64
from pw import ups_id, ups_pw, ups_api

#set connetion
settings = Settings(strict=False, xml_huge_tree=True)
client = Client('SCHEMA-WSDLs/LabelRecoveryWS.wsdl', settings=settings)

def UPS_reprint_label(tracking):
    #set soap headers
    headers = {

        'UPSSecurity':{
            'UsernameToken':{
                'Username':ups_id,
                'Password': ups_pw
            },
            'ServiceAccessToken' : {
            'AccessLicenseNumber':ups_api
            }
        }
    }
    # create request dictionary
    RequestDictionary = {
        'RequestOption': 'Request Option'
    }
    labelSepcificationDictionary = {
            "HTTPUserAgent": "Mozilla/4.5",
            "LabelImageFormat": {
                "Code": "ZPL",
                #"Description": "ZPL"
            },
            "LabelStockSize": {
                "Height": "6",
                "Width": "4"
            }
        }
    # try operation
    try:
        response = client.service.ProcessLabelRecovery(_soapheaders=headers, Request=RequestDictionary, LabelSpecification=labelSepcificationDictionary, TrackingNumber=tracking)   #    tracking
        # print(response)

        data = helpers.serialize_object(response, dict)
        data_to_string = str(data).strip()
        data_to_string = str(data).split(',')
        data_to_string = str(data).split('{')
        data_to_string = str(data).split("'")
        # print(data_to_string)

        base64_code = '-1'
        count = 0
        tracking = '-2'

        base64_code = str(str(data).split("'GraphicImage': '")[1]).split("'")[0]
        # print(f"base: {base64_code}")

        # for x in data_to_string:
        #     # count += 1
        #     if len(x) > 200:
        #         base64_code = x

        ups_label = base64.b64decode(base64_code)
        convert_zpl_Reprint(ups_label)

        done = "Done"
        return done

    except Fault as error:
        #print(ET.tostring(error.detail))
        error = ET.tostring(error.detail)

        data = str(str(error).split("Description>")[1]).split("<")[0]
        # print(error)
        return data