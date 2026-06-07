#entry point, orchestrates everything

from db.connection import get_connection
from db.create_tables import create_tables

def main():
    conn = get_connection()
    create_tables(conn)
    conn.close()
    print("Done!")

if __name__ == "__main__":
    main()