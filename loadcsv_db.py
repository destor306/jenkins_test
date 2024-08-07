import psycopg2
import csv

# Using psycopg2
def load_data_with_psycopg2():
    connection_string = "dbname='postgres' user='postgres' password='1234' host='172.208.27.131' port='5432'"
    csv_path_parcelid = "/app/parcel_id_to_pin_conversion_table.csv"
    csv_path_sales = "/app/latest_sales_data.csv"
    connection = None  # Initialize connection to None
    try:
        # Connect to the database
        connection = psycopg2.connect(connection_string)
        cursor = connection.cursor()

        # Drop tables if they exist
        cursor.execute("DROP TABLE IF EXISTS parcelidtopin")
        cursor.execute("DROP TABLE IF EXISTS latest_sales_data")

        # Create tables
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS parcelidtopin (
            parcel_id TEXT,
            pin TEXT
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS latest_sales_data (
            "ParcelID" TEXT,
            Sale_Date TEXT,
            Sale_Price TEXT,
            "PIN" TEXT,
            Alt_Key TEXT
        );
        """)

        # Load CSV data
        with open(csv_path_parcelid, 'r') as f:
            next(f)  # Skip the header row
            cursor.copy_expert("COPY parcelidtopin FROM STDIN WITH CSV HEADER DELIMITER ','", f)

        with open(csv_path_sales, 'r') as f:
            next(f)  # Skip the header row
            cursor.copy_expert("COPY latest_sales_data FROM STDIN WITH CSV HEADER DELIMITER ','", f)

        # Commit the changes
        connection.commit()

        print("CSV data loaded successfully with psycopg2!")
    except Exception as e:
        print(f"An error occurred during data processing: {e}")
    finally:
        if connection:
            cursor.close()
            connection.close()

# Uncomment one of the following lines to choose which method to use:
# load_data_with_sqlalchemy()
load_data_with_psycopg2()
