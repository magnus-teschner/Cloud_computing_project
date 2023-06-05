import json
from cc_functions import DataAccess

def test_insert_sale():
    data_access = DataAccess()

    # Testdaten
    input_data = '[{"products":[{"name":"Playstation 5","price":"599.99"},{"name":"Xbox Series X","price":"499.00"}],"name":"Max","discount":"40"}]'

    # JSON-Daten in ein Python-Objekt konvertieren
    data = json.loads(input_data)

    # Überprüfen, ob Daten vorhanden sind
    if len(data) > 0:
        customer = data[0]

        customer_name = customer['name']
        discount = customer['discount']

        products = customer['products']

        for product in products:
            product_name = product['name']
            product_price = product['price']

            # Verkaufsdaten in die Datenbank einfügen
            data_access.insert_sale(customer_name, discount, product_name, product_price)

        print("Testdaten wurden erfolgreich eingefügt")
    else:
        print("Keine Daten zum Einfügen vorhanden")

    # Instanz der DataAccess-Klasse bereinigen
    del data_access

# Testfunktion aufrufen
test_insert_sale()
