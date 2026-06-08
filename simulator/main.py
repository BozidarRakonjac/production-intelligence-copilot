#entry point, orchestrates everything

from db.connection import get_connection
from db.create_tables import create_tables
from loaders.telemetry_loader import load_telemetry
from loaders.downtime_loader import load_downtime
from loaders.quality_loader import load_quality

def main():
    conn = get_connection()
    create_tables(conn)
    load_telemetry(conn)
    load_downtime(conn)
    load_quality(conn)
    conn.close()
    print("Done!")

if __name__ == "__main__":
    main()