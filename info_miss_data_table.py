import pandas as pd

file_path = r"C:\Users\Sara\Desktop\Università\magistrale\Terzo_anno\Applied AI in biomedicine\progetto\training_metadata.xlsx"
df = pd.read_excel(file_path)

# Single groupby pass for both missingness and 1 vs 0 breakdown
summary = (
    df.groupby("Cohort ID", as_index=False)
    .agg(
        Total_People=("ID", "count"),
        Missing_MGMT=("MGMT value", lambda s: s.isna().sum()),
        Present_MGMT=("MGMT value", lambda s: s.notna().sum()),
        methylated=("MGMT value", lambda s: (s == 1).sum()),
        not_methylated=("MGMT value", lambda s: (s == 0).sum()),
    )
    .assign(
        miss_pct=lambda d: (d["Missing_MGMT"] / d["Total_People"] * 100).round(1),
        included_pct=lambda d: (d["Present_MGMT"] / d["Total_People"] * 100).round(1),
        diff_1_minus_0=lambda d: d["methylated"] - d["not_methylated"],
        pct_1_of_known=lambda d: (d["methylated"] / d["Present_MGMT"] * 100).round(1),
        pct_0_of_known=lambda d: (d["not_methylated"] / d["Present_MGMT"] * 100).round(1),
    )
)

print(summary)

# Save to the Excel file reusing file_path (and write known_comparison or both if needed)
with pd.ExcelWriter(file_path, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
    summary.to_excel(writer, sheet_name="mgmt_summary", index=False)