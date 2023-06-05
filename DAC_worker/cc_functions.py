import psycopg2

class DataAccess:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="Ort1mand"
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS sales (id SERIAL PRIMARY KEY, customer_name VARCHAR(50), discount VARCHAR(100), product_name VARCHAR(50), product_price VARCHAR(100));")
        self.conn.commit()

    def insert_sale(self, customer_name, discount, product_name, product_price):
        query = "INSERT INTO sales (customer_name, discount, product_name, product_price) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (customer_name, discount, product_name, product_price))
        self.conn.commit()
