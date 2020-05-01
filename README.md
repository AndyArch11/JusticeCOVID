# JusticeCOVID
 
To generate prison list:

Step 1

Run wikipedia_au_prison_parser.py, this will generate a new prison_list.csv.

If using an updated ABS reference file, then the script may need to be updated with new excel mappings for each state.

Step 2

Clean up content of prison_list.csv
    - manually merge duplicated prison entries where name match was not able to do so
    - determine lat/lon of prisons that don't have values
    - clean up any outstanding values

N.B. As this has already been done, it may be faster to merge via vlookup or other means any new output with existing.

Step 3

Run csv_to_json.py, this will generate prison_list.json containing operational prisons.

Step 4

Copy contents of prison_list.json into au_prison_map.html, replacing contents of const prison.

Step 5

View au_prison_map.html in browser.