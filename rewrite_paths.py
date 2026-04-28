#!/usr/bin/env python
# coding: utf-8

# REWRITE PATHS
# Replaces a Windows UNC path prefix in the CSV's "Full Path" column
# with a custom Linux-compatible path prefix.

import csv
import os

csv.field_size_limit(10000000)

# --- CONFIGURATION ---
input_csv  = r'./UMF_Database_image_list_1.csv'
output_csv = r'./UMF_Database_image_list_linux.csv'

# The Windows UNC prefix to strip (case-insensitive match)
WINDOWS_PREFIX = r'\\argos.storage.uu.se\MyGroups$\Bronze'

# The Linux prefix to substitute in
LINUX_PREFIX = '/opt/media/gust/Bronze'


def unc_to_linux(path: str, win_prefix: str, linux_prefix: str) -> str:
    """
    Replace a Windows UNC prefix with a Linux path prefix.

    Steps:
      1. Strip the known UNC prefix (case-insensitive).
      2. Replace every backslash with a forward slash.
      3. Prepend the Linux prefix.
      4. Collapse any accidental double slashes.
    """
    # Normalise to a consistent case for the prefix comparison
    if path.lower().startswith(win_prefix.lower()):
        remainder = path[len(win_prefix):]          # everything after the prefix
        remainder = remainder.replace('\\', '/')    # flip separators
        new_path  = linux_prefix + remainder        # attach new root
        new_path  = new_path.replace('//', '/')     # tidy up double slashes
        return new_path
    # Path did not match the expected prefix – return unchanged
    return path


def rewrite_csv(input_path: str, output_path: str) -> None:
    replaced = 0
    skipped  = 0

    with open(input_path,  mode='r', encoding='utf-8-sig') as infile, \
         open(output_path, mode='w', encoding='utf-8-sig', newline='') as outfile:

        first_line = infile.readline()
        infile.seek(0)
        delimiter = ';' if ';' in first_line else ','

        reader = csv.DictReader(infile, delimiter=delimiter)
        # Normalise field names (strip BOM / whitespace)
        reader.fieldnames = [n.strip().replace('\ufeff', '') for n in reader.fieldnames]

        writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames,
                                delimiter=delimiter, lineterminator='\n')
        writer.writeheader()

        for row in reader:
            original = row.get('Full Path', '')
            if original:
                converted = unc_to_linux(original, WINDOWS_PREFIX, LINUX_PREFIX)
                if converted != original:
                    row['Full Path'] = converted
                    replaced += 1
                else:
                    skipped += 1
            writer.writerow(row)

    print(f"✅ Done.")
    print(f"   Paths replaced : {replaced}")
    print(f"   Paths unchanged: {skipped}")
    print(f"   Output written : {os.path.abspath(output_path)}")


if __name__ == '__main__':
    rewrite_csv(input_csv, output_csv)
