# JusticeCOVID

See Reference.txt for sources used to generate the maps and graphs.

N.B. Each html file is standalone.  They can be downloaded and run from a local computer, but do require Internet access for Javascript libraries. The html files include inline Javascript. If these were to be executed from a webserver, it would be more efficient to extract the inline javascript into its own standalone file(s) and minimize the content.  

## Prison Map 
* au_prison_map.html
    * Shows a map of prisons across Australia
    * Prisons can be filtered
    * Under "Details" a table of prisons that have been filtered is also generated

To generate the prison list or update what is used in the html file:

### Step 1

Run wikipedia_au_prison_parser.py, this will generate a new prison_list.csv.

If using an updated ABS reference file, then the script may need to be updated with new excel mappings for each state.

### Step 2

Clean up content of prison_list.csv
* manually merge duplicated prison entries where name match was not able to do so - eg:
    * "Loddon Prison" in ABS data is "HM Prison Loddon" in Wikipedia
    * "High Risk Management Correctional Centre" in ABS data is a prison within the "Goulburn Correctional Centre" prison complex in Wikipedia
* determine lat/lon of prisons that don't have values
* clean up any outstanding values
* update Max field to have the max value of either Capacity or Males + Females.

N.B. As this has already been done, it may be faster to merge via vlookup or other means, any new output with existing csv.

### Step 3

Run csv_to_json.py, this will generate prison_list.json containing operational prisons.
* "Public/Private" column needs to be renamed to "PublicPrivate" - TODO to change code

### Step 4

Copy contents of prison_list.json into au_prison_map.html, replacing contents of const prison.

### Step 5

View au_prison_map.html in browser.

## Population

Generates various graphs of the Australian Prisoner population.

* au_prison_seir.html
    * Similar to seir_google.html and seir_plotly.html, more customisable with parameters available to model a coronavirus infection within an Australian prison - with prisons available via drop down.
    * Uses the same prison list as au_prison_map.html
* covid19_prisoner_impact.hml
    * Applies what is known of COVID-19 against what is known of the Australian prison population to provide some insights on the extent of the potential impact of COVID-19 on the Australian prison population.
* prisoner_health.html
    * Some graphs of what is known of the Australian prison population with regard to health factors that can contribute to negative outcomes in relation to COVID-19.
* prison_population.html
    * Graphs of what is known of the Australian prison population.
* seir_google.html
    * A SEIR model of the spread of coronavirus through a population of a given size.  
    * Parameters are defaulted to what we have seen so far in Australia with respect to COVID-19, but can be adjusted.
    * Uses Google charts
* seir_plotly.html
    * Same as seir_google.html, but uses Plotly javascript charts

### Data

There are various speadsheets of source material used that have been downloaded to act as a point in time snapshot.

See _Population Indicators.xlsx_ for the logic used to combine this data that is subsequently used in the various graphs.

