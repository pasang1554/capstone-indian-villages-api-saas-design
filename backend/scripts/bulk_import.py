import pandas as pd
from sqlalchemy import create_engine, text
import sys

def bulk_import(csv_path, db_url):
    engine = create_engine(db_url)
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["state_name", "district_name", "sub_district_name", "village_name"])

    print(f"Importing {len(df)} rows...")
    with engine.begin() as conn:
        # Insert countries
        conn.execute(text("INSERT OR IGNORE INTO countries (name, code) VALUES ('India', 'IN')"))
        india_id = conn.execute(text("SELECT id FROM countries WHERE code='IN'")).scalar()

        # Get unique states
        states = df[["state_name", "state_code"]].drop_duplicates()
        for _, row in states.iterrows():
            conn.execute(
                text("INSERT OR IGNORE INTO states (name, code, country_id) VALUES (:name, :code, :cid)"),
                {"name": row["state_name"], "code": str(row.get("state_code", "")), "cid": india_id}
            )

        # Get unique districts
        districts = df[["state_name", "district_name"]].drop_duplicates()
        for _, row in districts.iterrows():
            state_id = conn.execute(text("SELECT id FROM states WHERE name=:name"), {"name": row["state_name"]}).scalar()
            if state_id:
                conn.execute(
                    text("INSERT OR IGNORE INTO districts (name, state_id) VALUES (:name, :sid)"),
                    {"name": row["district_name"], "sid": state_id}
                )

        # Get unique sub-districts
        sub_dists = df[["district_name", "sub_district_name"]].drop_duplicates()
        for _, row in sub_dists.iterrows():
            dist_id = conn.execute(text("SELECT id FROM districts WHERE name=:name"), {"name": row["district_name"]}).scalar()
            if dist_id:
                conn.execute(
                    text("INSERT OR IGNORE INTO sub_districts (name, district_id) VALUES (:name, :did)"),
                    {"name": row["sub_district_name"], "did": dist_id}
                )

        # Bulk insert villages
        count = 0
        for _, row in df.iterrows():
            sub = conn.execute(text("SELECT id FROM sub_districts WHERE name=:name"), {"name": row["sub_district_name"]}).scalar()
            dist = conn.execute(text("SELECT id FROM districts WHERE name=:name"), {"name": row["district_name"]}).scalar()
            state = conn.execute(text("SELECT id FROM states WHERE name=:name"), {"name": row["state_name"]}).scalar()
            if sub and dist and state:
                conn.execute(
                    text("INSERT OR IGNORE INTO villages (name, village_code, sub_district_id, district_id, state_id) VALUES (:name, :code, :sub, :dist, :st)"),
                    {"name": row["village_name"], "code": str(row.get("village_code", "")), "sub": sub, "dist": dist, "st": state}
                )
                count += 1
                if count % 10000 == 0:
                    print(f"  ... {count} villages inserted")

    print(f"Imported {len(df)} rows into database.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python bulk_import.py <csv_file> <db_url>")
        sys.exit(1)
    bulk_import(sys.argv[1], sys.argv[2])
