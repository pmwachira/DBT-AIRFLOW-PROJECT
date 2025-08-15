from api_request import mock_api_request
import psycopg2

def connect_to_db():
    print('connecting to db..')
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5000,
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

print(connect_to_db())