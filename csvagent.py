import csv
import os

input_folder = "D:\de ar csv"
output_master_raw = "german_arabic_master_18000_raw.csv"
output_master_ready = "german_arabic_master_ready.csv"

all_rows_raw = []
all_rows_ready = []

# Loop through vol1.csv to vol6.csv
for i in range(1, 7):
    filename = f"vol{i}.csv"
    filepath = os.path.join(input_folder, filename)
    
    # Fallback to direct volume file names if outside folder
    if not os.path.exists(filepath):
        filepath = f"german_arabic_3000_vol{i}_raw.csv"

    if os.path.exists(filepath):
        with open(filepath, mode="r", encoding="utf-8-sig") as infile:
            reader = csv.DictReader(infile)
            for row in reader:
                word = row.get("Word", "").strip()
                word_type = row.get("Type", "").strip()
                meaning = row.get("Meaning", row.get("Definition", "")).strip()

                if word:
                    all_rows_raw.append([word, word_type, meaning])
                    html_def = f'<div dir="rtl" align="right"><b>{meaning}</b> ({word_type})</div>' if word_type else f'<div dir="rtl" align="right"><b>{meaning}</b></div>'
                    all_rows_ready.append([word, html_def])

# Save merged RAW CSV
with open(output_master_raw, mode="w", encoding="utf-8-sig", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Word", "Type", "Meaning"])
    writer.writerows(all_rows_raw)

# Save merged PyGlossary READY CSV
with open(output_master_ready, mode="w", encoding="utf-8-sig", newline="") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(["Word", "Definition"])
    writer.writerows(all_rows_ready)

print(f" Total words processed and merged: {len(all_rows_raw)}")
print(f" Master RAW file saved to: {output_master_raw}")
print(f" PyGlossary READY file saved to: {output_master_ready}")
