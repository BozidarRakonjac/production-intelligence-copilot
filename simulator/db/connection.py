#PostgreSQL connection

import psycopg2
import os
import time

def get_connection():
    # retry logic because PostgreSQL container might not be ready yet
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                host=os.getenv("POSTGRES_HOST"),
                port=os.getenv("POSTGRES_PORT"),
                user=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
                dbname=os.getenv("POSTGRES_DB")
            )
            print("Connected to PostgreSQL")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Connection failed, retrying... {retries} attempts left")
            retries -= 1
            time.sleep(3)
    raise Exception("Could not connect to PostgreSQL after 5 retries")