import pandas as pd
import os
import glob

DATASET_DIR = "dataset"
OUTPUT_FILE = "data/all_india_villages.csv"

def extract_state_name(filename):
    # Rdir_2011_29_KARNATAKA.xls -> KARNATAKA
    parts = filename.replace(".xls", "").replace(".ods", "").split("_")
    return parts[-1] if parts else "UNKNOWN"

def clean_dataframe(df, state_name):
    # Expected columns: STATE NAME, DISTRICT NAME, SUB-DISTRICT NAME, Area Name
    # Map to standard names
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]

    # Required columns mapping
    col_map = {
        "STATE NAME": "state_name",
        "DISTRICT NAME": "district_name",
        "SUB-DISTRICT NAME": "sub_district_name",
        "Area Name": "village_name",
        "MDDS PLCN": "village_code",
        "MDDS STC": "state_code",
        "MDDS DTC": "district_code",
        "MDDS Sub_DT": "sub_district_code"
    }

    df = df.rename(columns=col_map)
    df["state_name"] = state_name

    # Keep only needed columns
    keep_cols = ["state_name", "state_code", "district_name", "district_code",
                 "sub_district_name", "sub_district_code", "village_name", "village_code"]
    for col in keep_cols:
        if col not in df.columns:
            df[col] = ""

    return df[keep_cols]

def main():
    files = sorted(glob.glob(os.path.join(DATASET_DIR, "*.xls")) +
                   glob.glob(os.path.join(DATASET_DIR, "*.ods")))
    print(f"Found {len(files)} files")

    all_dfs = []
    for f in files:
        state_name = extract_state_name(os.path.basename(f))
        try:
            if f.endswith(".ods"):
                df = pd.read_excel(f, engine="odf")
            else:
                df = pd.read_excel(f, engine="xlrd")
            cleaned = clean_dataframe(df, state_name)
            all_dfs.append(cleaned)
            print(f"  ✓ {state_name}: {len(cleaned)} rows")
        except Exception as e:
            print(f"  ✗ {state_name}: {e}")

    if all_dfs:
        merged = pd.concat(all_dfs, ignore_index=True)
        os.makedirs("data", exist_ok=True)
        merged.to_csv(OUTPUT_FILE, index=False)
        print(f"\n✓ Merged {len(merged)} rows into {OUTPUT_FILE}")
        print(f"  States: {merged['state_name'].nunique()}")
        print(f"  Villages with names: {(merged['village_name'] != '').sum()}")
    else:
        print("No data processed!")

if __name__ == "__main__":
    main()
