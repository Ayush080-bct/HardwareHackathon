import pandas as pd

# Load raw data
df = pd.read_csv("../raw/power_data.csv")

# Pivot → one row per timestamp
wide = df.pivot(
    index=["timestamp","hour"],
    columns="house_id",
    values="current"
).reset_index()

# Rename columns
wide.columns = [
    "timestamp","hour",
    "house1_current",
    "house2_current",
    "house3_current",
    "house4_current",
    "house5_current"
]

# Feature engineering
wide["total_current"] = wide[
    [c for c in wide.columns if "house" in c]
].sum(axis=1)

wide["is_peak_hour"] = wide["hour"].isin(
    [6,7,8,18,19,20,21]
).astype(int)

wide["current_change_rate"] = wide["total_current"].diff().fillna(0)

# Labels (physics-based)
wide["overload_flag"] = (wide["total_current"] > 18).astype(int)
wide["main_contributor"] = wide[
    [c for c in wide.columns if "house" in c]
].idxmax(axis=1).str.extract(r'(\d)').astype(int)

# Save processed dataset
wide.to_csv("./train_data.csv", index=False)

print("✅ Processed ML dataset saved: data/processed/train_data.csv")
