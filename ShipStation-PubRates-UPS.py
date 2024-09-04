import requests
import json
import base64
import pandas as pd

# Replace with your ShipStation API Key and Secret
API_KEY = '5676ad9fe8dc41b19f2deff0b2563a61'
API_SECRET = '04b38e32df8749e3b6452cff50a974c8'

# Encode credentials to Base64
credentials = f'{API_KEY}:{API_SECRET}'
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

# ShipStation API base URL
BASE_URL = 'https://ssapi.shipstation.com'

# Sample address dataset
dataset = "EB-ShipStation.csv"
address_dataset = pd.read_csv(dataset)


def get_published_rate(address):
    url = f"{BASE_URL}/shipments/getrates"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic {encoded_credentials}'
    }

    # Shipment data structure for UPS Ground
    shipment_data = {
        "carrierCode": address['carrier'],
        "serviceCode": address['service'],
        "packageCode": "package",
        "fromPostalCode": "01803",  # Replace with your from postal code
        "toCountry": address['country'],
        "toPostalCode": address['postalCode'],
        "toState": address['state'],
        "toCity": address['city'],
        "toStreet1": address['street1'],
        "weight": {
            "value": address['weight'],  # Replace with the weight of your package
            "units": "pounds"
        },
        "dimensions": {
            "units": "inches",
            "length": address['length'],
            "width": address['width'],
            "height": address['height']
        },
        "confirmation": "delivery",
        "residential": True
    }

    response = requests.post(url, headers=headers, data=json.dumps(shipment_data))
    
    if response.status_code == 200:
        rates = response.json()
        if rates:
            return rates[0]['shipmentCost'] + rates[0]['otherCost']# Return the first rate
        else:
            return "No rates found"
    else:
        return f"Error: {response.status_code} - {response.text}"

def main():
    rates_list = []
    for index, row in address_dataset.iterrows():
        postal_code = str(row['Ship Postal Code'])
        if len(postal_code) == 4:
            postal_code = '0' + postal_code
        lb_weight = row["Weight Oz"]/16

        new_carrier = row['Carrier']
        new_service = row['Shipping Service']
        if new_carrier == "UPS" and new_service == "Ground":
            new_carrier = "ups"
            new_service = "ups_ground"
        elif new_carrier == "FedEx" and new_service == "Ground":
            new_carrier = "fedex"
            new_service = "fedex_home_delivery"
        elif new_carrier == "USPS" and new_service == "MM":
            new_carrier = "stamps_com"
            new_service = "usps_media_mail"


        address = {
            "name": row['Ship Name'],
            "street1": row['Ship Street 1'],
            "city": row['Ship City'],
            "state": row['Ship State'],
            "postalCode": postal_code,
            "country": row['Ship Country'],
            "length": row['Package Length'],
            "width": row['Package Width'],
            "height": row['Package Height'],
            "weight": lb_weight,
            "carrier": new_carrier,
            "service": new_service

        }
        rate = get_published_rate(address)
        rates_list.append(rate)
        print(f"Shipping rate for {new_carrier} {new_service} {address['name']} at {address['street1']}, {address['city']}, {address['state']} {address['postalCode']} is:")
        print(f'${rate}')
        print(lb_weight)
        print()

    # Add rates to the dataset and export to CSV
    address_dataset['Rates'] = rates_list

    new_dataset = address_dataset[['Order Number', 'Order Date', 'Ship Name', 'Ship Company', 'Ship Street 1', 'Ship Street 2', 'Ship City', 'Ship State', 'Ship Postal Code', 'Ship Country', 'Ship Phone', 'Carrier', 'Shipping Service', 'Tracking Number', 'Carrier Fee', 'Rates']]
    
    new_dataset.to_csv('ShipStationPubRates.csv', index=False)

if __name__ == '__main__':
    main()