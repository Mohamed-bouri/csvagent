import csv
import os
import glob

# --- CONFIGURATION ---
# Using 'r' before the string prevents backslash escape errors in Windows paths
INPUT_FOLDER = r"D:\de ar csv" # غيره بالمسار الخاص بك
OUTPUT_MASTER_RAW = "german_arabic_master_raw.csv" # غيره ب الخاص بك
OUTPUT_MASTER_READY = "german_arabic_master_ready.csv" # غيره ب الخاص بك

def merge_dictionaries():
    all_rows_raw = []
    all_rows_ready = []
    seen_words = set()  # Tracks words we've already added to prevent duplicates

    # 1. DYNAMIC DISCOVERY: Find all .csv files in the folder automatically
    search_pattern = os.path.join(INPUT_FOLDER, "*.csv")
    csv_files = glob.glob(search_pattern)

    if not csv_files:
        print(f"⚠️ No CSV files found in: {INPUT_FOLDER}")
        return

    print(f"Found {len(csv_files)} CSV files. Starting merge...\n")

    for filepath in csv_files:
        # Prevent the script from reading its own output files if they are in the same folder
        if filepath.endswith((OUTPUT_MASTER_RAW, OUTPUT_MASTER_READY)):
            continue

        print(f"Processing: {os.path.basename(filepath)}")
        
        # 2. ERROR HANDLING: Safely try to open and read the file
        try:
            with open(filepath, mode="r", encoding="utf-8-sig") as infile:
                reader = csv.DictReader(infile)
                
                # Check if the file has the expected headers before processing
                headers = reader.fieldnames or []
                if "Word" not in headers:
                    print(f"  -> ⚠️ Skipping: Missing 'Word' column.")
                    continue

                for row in reader:
                    word = row.get("Word", "").strip()
                    word_type = row.get("Type", "").strip()
                    meaning = row.get("Meaning", row.get("Definition", "")).strip()

                    # 3. DUPLICATE PREVENTION: Only add if we haven't seen this word yet
                    if word and word not in seen_words:
                        seen_words.add(word)
                        all_rows_raw.append([word, word_type, meaning])

                        # HTML formatting for RTL Arabic
                        if word_type:
                            html_def = f'<div dir="rtl" align="right"><b>{meaning}</b> ({word_type})</div>'
                        else:
                            html_def = f'<div dir="rtl" align="right"><b>{meaning}</b></div>'
                        
                        all_rows_ready.append([word, html_def])

        except Exception as e:
            print(f"  -> ❌ Error reading file: {e}")

    # Save merged RAW CSV
    with open(OUTPUT_MASTER_RAW, mode="w", encoding="utf-8-sig", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Word", "Type", "Meaning"])
        writer.writerows(all_rows_raw)

    # Save merged PyGlossary READY CSV
    with open(OUTPUT_MASTER_READY, mode="w", encoding="utf-8-sig", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(["Word", "Definition"])
        writer.writerows(all_rows_ready)

    print("\n✅ Merge Complete!")
    print(f" -> Total unique words processed: {len(all_rows_raw)}")
    print(f" -> Master RAW file saved to: {OUTPUT_MASTER_RAW}")
    print(f" -> PyGlossary READY file saved to: {OUTPUT_MASTER_READY}")

# Run the function
if __name__ == "__main__":
    merge_dictionaries()
