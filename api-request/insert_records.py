import psycopg2
from api_request import feath_data, mock_fetch_data

def connect_to_db():

    print("Connecting to the database...")

    try:
        conn = psycopg2.connect(
            host="db",
            port="5432",
            database="db",
            user="db_user",
            password="db_password"
        )
        print("Connected to the database successfully .... 😊")
        return conn
        
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


def create_table(conn):
    print("Creating table...")
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city text,
                temperature Float,
                weather_descriptions text,
                wind_speed Float,
                time Timestamp,
                insert_at Timestamp DEFAULT NOW(),
                utc_offset text
            );
        """)
        cursor.execute("""
            ALTER TABLE dev.raw_weather_data
            ADD COLUMN IF NOT EXISTS insert_at TIMESTAMP DEFAULT NOW();
        """)
        cursor.execute("""
            ALTER TABLE dev.raw_weather_data
            ADD COLUMN IF NOT EXISTS utc_offset text;
        """)
        conn.commit()
        print("Table created successfully .... 😊")
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")
        conn.rollback()
        return None


def insert_record(conn,data):
    print("Inserting record...")

    try:
        cursor = conn.cursor()
        weather = data["current"]
        location = data["location"]

        cursor.execute("""
        INSERT INTO dev.raw_weather_data (
        city,
        temperature,
        weather_descriptions,
        wind_speed,
        time,
        insert_at,
        utc_offset)
        
        VALUES (%s, %s, %s, %s, %s, NOW(), %s)
        """,(
            location["name"],
            weather["temperature"],
            weather["weather_descriptions"][0],
            weather["wind_speed"],
            location["localtime"],
            location["utc_offset"],
        )) 
        conn.commit()
        print("Record inserted successfully .... 😊")
    except psycopg2.Error as e:
        print(f"Error inserting record: {e}")
        conn.rollback()
        raise



def main (): 

    try:
        # data = mock_fetch_data()
        data = feath_data()
        conn = connect_to_db()
        create_table(conn)
        insert_record(conn,data)
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        raise

    finally:
        if "conn" in locals() and conn is not None:
            conn.close()
            print("Connection closed .... 😊")
