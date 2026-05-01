import pandas as pd
import sys

def audit_dataset(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    report = {
        "total_rows": len(df),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "columns": list(df.columns),
    }

    print("=== Data Audit Report ===")
    print(f"Total Rows: {report['total_rows']}")
    print(f"Duplicates: {report['duplicates']}")
    print(f"Columns: {report['columns']}")
    print("\nMissing Values:")
    for col, count in report["missing_values"].items():
        if count > 0:
            print(f"  {col}: {count} ({count/len(df)*100:.2f}%)")

    required = ["state_name", "district_name", "sub_district_name", "village_name"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        print(f"\nMissing required columns: {missing}")
    else:
        print("\nAll required columns present.")

    clean = df.drop_duplicates()
    clean = clean.dropna(subset=required, how="any")
    print(f"\nClean rows: {len(clean)} (removed {len(df) - len(clean)})")
    clean.to_csv(file_path.replace(".csv", "_cleaned.csv"), index=False)
    print(f"Saved cleaned data to {file_path.replace('.csv', '_cleaned.csv')}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python audit_cleaned_data.py <csv_file>")
        sys.exit(1)
    audit_dataset(sys.argv[1])
