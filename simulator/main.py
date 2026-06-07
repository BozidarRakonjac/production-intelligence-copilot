#entry point, orchestrates everything

from db.connection import get_connection
from db.create_tables import create_tables
from loaders.telemetry_loader import load_telemetry

def main():
    conn = get_connection()
    create_tables(conn)
    load_telemetry(conn)
    conn.close()
    print("Done!")

if __name__ == "__main__":
    main()