from datetime import datetime
import pandas as pd


def insert_data(ticketNumber, email, carrier, tracking, delivered, deliveryDate, sendEmailDate,
                chargeEmail):
    df = pd.read_csv('warranty_email.csv', index_col=False)

    # inputDate = datetime.strptime(inputDate,'%Y-%m-%d')
    # inputDate = inputDate.date()
    info = {
        # 'inputDate': [inputDate],
        'ticketNumber': [ticketNumber],
        'email': [email],
        'carrier': [carrier],
        'tracking': [tracking],
        'delivered': [delivered],
        'deliveryDate': [deliveryDate],
        'sendEmailDate': [sendEmailDate],
        # 'ticketStatus': [ticketStatus],
        'chargeEmail': [chargeEmail]
    }

    df_temp = pd.DataFrame(info)
    df = df.append(df_temp)

    df.to_csv('warranty_email.csv', index=False)

    print("Customer's info saved.")


def delete(col_name, val):
    df = pd.read_csv('warranty_email.csv', index_col=False)

    delete_row = df[df[col_name] == val].index
    df = df.drop(delete_row)

    df.to_csv('warranty_email.csv', index=False)
