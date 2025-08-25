from api_request import mock_api_request, make_api_request
import psycopg2

def connect_to_db():
    print('connecting to db..')
    try:
        conn = psycopg2.connect(
            host="db",
            port=5432,
            database="db",
            user="db_user",
            password="db_password"
        )
        print('connected to db')
        return conn
    except psycopg2.Error as e:
        print(f'Error connecting to db: {e}')
        raise
    except Exception as f:
        print(f'Error connecting to db: {f}')
        raise

def create_table(conn):
    print('creating table...')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE SCHEMA IF NOT EXISTS dev;
                       
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city text,
                temperature float,
                weather_description text,
                wind_speed float,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                utc_offset TEXT
            );
        ''')
        conn.commit()
        print('table created')
    except psycopg2.Error as e:
        print(f'Error creating table: {e}')
        conn.rollback()
        raise
    except Exception as f:
        print(f'Error creating table: {f}')
        conn.rollback()
        raise

def store_data(conn, data):
    print('storing data...')
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO dev.raw_weather_data (city, temperature, weather_description, wind_speed, time, inserted_at, utc_offset)
            VALUES (%s, %s, %s, %s, %s, NOW(), %s);
        ''', (
            data['location']['name'],
            data['current']['temperature'],
            ', '.join(data['current']['weather_descriptions']),
            data['current']['wind_speed'],
            data['location']['localtime'],
            data['location']['utc_offset']
        ))
        conn.commit()
        print('data stored successfully')
    except psycopg2.Error as e:
        print(f'Error storing data: {e}')
        conn.rollback()
        raise
    except Exception as f:
        print(f'Error storing data: {f}')
        conn.rollback()
        raise

def main():
    try:
        data = make_api_request()
        conn = connect_to_db()
        create_table(conn)
        inserted_data = store_data(conn, data)
    except Exception as e:
        print(f'Error in main: {e}')
    finally:
        if 'conn' in locals():
            conn.close()

