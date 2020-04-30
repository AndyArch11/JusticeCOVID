from lxml import html
import requests
import csv
import re
import pandas as pd

def dms2dec(dms_str):
    dec_value = ''

    dms_str = re.sub(r'\s', '', dms_str)
    
    sign = -1 if re.search('[swSW]', dms_str) else 1
    
    numbers = [*filter(len, re.split(r'\D+', dms_str, maxsplit=4))]

    if len(numbers) > 0:
        degree = numbers[0]
        minute = numbers[1] if len(numbers) >= 2 else '0'
        second = numbers[2] if len(numbers) >= 3 else '0'
        frac_seconds = numbers[3] if len(numbers) >= 4 else '0'
        
        second += "." + frac_seconds

        dec_value = sign * (int(degree) + float(minute) / 60 + float(second) / 3600)
    
    return dec_value

def signdec(unsigned_dec):
    dec_value = ''

    dec_str = re.sub(r'\s', '', unsigned_dec)

    sign = -1 if re.search('[swSW]', unsigned_dec) else 1

    dec_value = sign * (float(dec_str[0:-2])) #deleting °S or °E, should be more robust to cater for missing cardinal

    return dec_value

def getGeo(htmlpage):
    prison_geodec = []
    prison_lat = 0
    prison_lon = 0
    prison_geodec_span = htmlpage.xpath('//span[@class="geo-dec"]/text()')
    if len(prison_geodec_span) > 0:
        prison_geodec = prison_geodec_span[0].split(' ')
        if len(prison_geodec) > 0:
            prison_lat = signdec(prison_geodec[0])
            prison_lon = signdec(prison_geodec[1])
    else: #span[@class="geo-dms"]
        coord = ''
        coord = htmlpage.xpath('//span[@class="latitude"]/text()')
        if len(coord) > 0:
            prison_lat = dms2dec(coord[0])
            coord = ''
            coord = htmlpage.xpath('//span[@class="longitude"]/text()')
            if len(coord) > 0:
                prison_lon = dms2dec(coord[0])
    
    return prison_lat, prison_lon

#retrieve the ABS count of prisoners by prison for 2019
abs_nsw_male_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=7, nrows=42, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_nsw_male_prisons['Sex'] = 'Male'
abs_nsw_male_prisons['State'] = 'New South Wales'
abs_prison_df = pd.DataFrame(abs_nsw_male_prisons)
abs_nsw_female_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=51, nrows=14, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_nsw_female_prisons['Sex'] = 'Female'
abs_nsw_female_prisons['State'] = 'New South Wales'
abs_prison_df = abs_prison_df.append(abs_nsw_female_prisons, ignore_index=True)
abs_vic_male_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=69, nrows=13, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_vic_male_prisons['Sex'] = 'Male'
abs_vic_male_prisons['State'] = 'Victoria'
abs_prison_df = abs_prison_df.append(abs_vic_male_prisons, ignore_index=True)
abs_vic_female_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=84, nrows=2, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_vic_female_prisons['Sex'] = 'Female'
abs_vic_female_prisons['State'] = 'Victoria'
abs_prison_df = abs_prison_df.append(abs_vic_female_prisons, ignore_index=True)
abs_qld_male_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=90, nrows=13, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_qld_male_prisons['Sex'] = 'Male'
abs_qld_male_prisons['State'] = 'Queensland'
abs_prison_df = abs_prison_df.append(abs_qld_male_prisons, ignore_index=True)
abs_qld_female_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=105, nrows=6, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_qld_female_prisons['Sex'] = 'Female'
abs_qld_female_prisons['State'] = 'Queensland'
abs_prison_df = abs_prison_df.append(abs_qld_female_prisons, ignore_index=True)
abs_sa_male_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=115, nrows=9, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_sa_male_prisons['Sex'] = 'Male'
abs_sa_male_prisons['State'] = 'South Australia'
abs_prison_df = abs_prison_df.append(abs_sa_male_prisons, ignore_index=True)
abs_sa_female_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=126, nrows=3, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_sa_female_prisons['Sex'] = 'Female'
abs_sa_female_prisons['State'] = 'South Australia'
abs_prison_df = abs_prison_df.append(abs_sa_female_prisons, ignore_index=True)
abs_wa_male_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=133, nrows=13, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_wa_male_prisons['Sex'] = 'Male'
abs_wa_male_prisons['State'] = 'Western Australia'
abs_prison_df = abs_prison_df.append(abs_wa_male_prisons, ignore_index=True)
abs_wa_female_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=148, nrows=8, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_wa_female_prisons['Sex'] = 'Female'
abs_wa_female_prisons['State'] = 'Western Australia'
abs_prison_df = abs_prison_df.append(abs_wa_female_prisons, ignore_index=True)
abs_tas_male_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=160, nrows=4, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_tas_male_prisons['Sex'] = 'Male'
abs_tas_male_prisons['State'] = 'Tasmania'
abs_prison_df = abs_prison_df.append(abs_tas_male_prisons, ignore_index=True)
abs_tas_female_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=166, nrows=2, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_tas_female_prisons['Sex'] = 'Female'
abs_tas_female_prisons['State'] = 'Tasmania'
abs_prison_df = abs_prison_df.append(abs_tas_female_prisons, ignore_index=True)
abs_nt_male_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=172, nrows=4, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_nt_male_prisons['Sex'] = 'Male'
abs_nt_male_prisons['State'] = 'Northern Territory'
abs_prison_df = abs_prison_df.append(abs_nt_male_prisons, ignore_index=True)
abs_nt_female_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=178, nrows=2, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_nt_female_prisons['Sex'] = 'Female'
abs_nt_female_prisons['State'] = 'Northern Territory'
abs_prison_df = abs_prison_df.append(abs_nt_female_prisons, ignore_index=True)
abs_act_male_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=184, nrows=1, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_act_male_prisons['Sex'] = 'Male'
abs_act_male_prisons['State'] = 'Australian Capital Territory'
abs_prison_df = abs_prison_df.append(abs_act_male_prisons, ignore_index=True)
abs_act_female_prisons = pd.read_excel('./ABS Prisoners in Australia 2019 4517do002_2019.xls', sheet_name='Table_34', usecols='A:B', skiprows=187, nrows=1, index_col=None, header=None, names=['Prison', 'Prisoners'])
abs_act_female_prisons['Sex'] = 'Female'
abs_act_female_prisons['State'] = 'Australian Capital Territory'
abs_prison_df = abs_prison_df.append(abs_act_female_prisons, ignore_index=True)

#retrieve the prisons, prison capapacity, and prison locations from wikipedia
base_url = 'https://en.wikipedia.org'

page = requests.get(base_url + '/wiki/List_of_prisons_in_Australia')
html_content = html.fromstring(page.content)
html_content = html.make_links_absolute(html_content, base_url, False)

prison_tables = html_content.xpath('//div[@id="mw-content-text"]/div/table', smart_strings=False)

prison_list = []
prison_details = []
prison_detail_columns = ['State', 'Prison', 'Status', 'Managed', 'Public/Private', 'Capacity', 'Males', 'Females', 'Latitude', 'Longitude']
prison_column = 0
status_column = 1
managed_column = 3
capacity_column = 6
location_column = 7

state = ''
row_count = 0

#iterate through each state table listing that state's prisons
for state_prisons in prison_tables:
    prisons = state_prisons.xpath('./tbody/tr', smart_strings=False)

    prison = ''
    status = ''
    capacity = ''
    location = ''
    managedby = ''
    for row in prisons:
        #Get the state from the first row in each table, which is determined by only having a single merged column
        if len(row) == 1:
            state_attribute = row.xpath('./th/a[@title]/text()', smart_strings=False)
            if len(state_attribute) == 1:
                state = state_attribute[0].strip()
                print('')
                print('State')
                print(state)
                print('')
                row_count = 1
        elif len(row) == 8 and row_count == 1:
            #skip the second row which is only the table headers
            row_count += 1
        elif (len(row) == 7 or len(row) == 8) and row_count > 1:
            #iterate through the table rows, getting the details per prison
            prison_lat = 0
            prison_lon = 0

            #Cater for the 4th column "Managed" having merged rows, which for subsequent rows to the first merged one, leaves one less column
            if len(row) == 7:
                column_offset = -1
            elif len(row) == 8:
                column_offset = 0

            print('')
            print('Prison')
            prison = row[prison_column]
            prison_name = prison.text_content().strip().rstrip('[0123456789]')
            print(prison_name)
            #first attempt to get the geocoords from the left hand prison link, which will be more specific
            for prison_elements in prison:
                prison_attributes = prison_elements.items()
                for attr in prison_attributes:
                    if attr[0] == 'href':
                        print('href: ' + attr[1])
                        href = attr[1]
                        prison_page = requests.get(href)
                        prison_html_content = html.fromstring(prison_page.content)

                        prison_lat, prison_lon = getGeo(prison_html_content)
            
            print('Status')
            status = row[status_column].text_content().strip().rstrip('[0123456789]')
            print(status)
            print('Managed')
            if len(row) == 8:
                #only use the value from the first row of the merged columns.
                managedby = row[managed_column].text_content().strip()
            print(managedby)     
            print('Public/Private')
            if 'geo' in managedby.lower() or 'serco' in managedby.lower() or 'g4s' in managedby.lower() or 'sodexo' in managedby.lower():
                pubpriv = 'Private'
            else:
                pubpriv = 'Public'
            print(pubpriv)
            print('Capacity')
            capacity = row[capacity_column + column_offset].text_content().strip()
            print(capacity)
            print('Location')
            location = row[location_column + column_offset]
            print(location.text_content().strip().rstrip('[0123456789]'))
            #if unable to get the geocoords from the prison link, try getting them from the right hand less accurate Location link
            if prison_lat == 0 and prison_lon == 0:
                for location_elements in location:
                    location_attributes = location_elements.items()
                    for attr in location_attributes:
                        if attr[0] == 'href':
                            print('href: ' + attr[1])
                            href = attr[1]
                            
                            location_page = requests.get(href)
                            location_html_content = html.fromstring(location_page.content)
                            
                            prison_lat, prison_lon = getGeo(location_html_content)

            print('Prison Latitude: ' + str(prison_lat))
            print('Prison Longitude: ' + str(prison_lon))

            prison_details = [state, prison_name, status, managedby, pubpriv, capacity, 0, 0, prison_lat, prison_lon]
            prison_list.append(prison_details)

            row_count += 1


#['State', 'Prison', 'Status', 'Managed', 'Public/Private', 'Capacity', 'Males', 'Females', 'Latitude', 'Longitude']

#merge abs data with wikipedia data
wiki_prison_df = pd.DataFrame(prison_list, columns=prison_detail_columns)
print(abs_prison_df)
print(wiki_prison_df)
for index, state_prison in abs_prison_df.iterrows():
    print(state_prison)
    print('State: ' + state_prison['State'] + ', Prison: ' + state_prison['Prison'] + ', Prisoners: ' + str(state_prison['Prisoners']) + ', Sex: ' + state_prison['Sex'])
    if len(wiki_prison_df.loc[(wiki_prison_df['State'] == state_prison['State']) & (wiki_prison_df['Prison'] == state_prison['Prison'])]) > 0:
        #if match, update record with prisoners count
        print(wiki_prison_df.loc[(wiki_prison_df['State'] == state_prison['State']) & (wiki_prison_df['Prison'] == state_prison['Prison'])])
        if state_prison['Sex'] == 'Male':
            wiki_prison_df.loc[(wiki_prison_df['State'] == state_prison['State']) & (wiki_prison_df['Prison'] == state_prison['Prison']), 'Males'] = state_prison['Prisoners']
        elif state_prison['Sex'] == 'Female':
            wiki_prison_df.loc[(wiki_prison_df['State'] == state_prison['State']) & (wiki_prison_df['Prison'] == state_prison['Prison']), 'Females'] = state_prison['Prisoners']        
        print(wiki_prison_df.loc[(wiki_prison_df['State'] == state_prison['State']) & (wiki_prison_df['Prison'] == state_prison['Prison'])])
    else:
        #if no match, add new record to the dataframe
        if state_prison['Sex'] == 'Male':
            wiki_prison_df = wiki_prison_df.append({'State': state_prison['State'], 'Prison': state_prison['Prison'], 'Status': 'Operational (ABS)', 'Managed': 'Unknown', 'Public/Private': '?', 'Capacity': '?', 'Males': state_prison['Prisoners'], 'Females': 0, 'Latitude': 0, 'Longitude': 0}, ignore_index=True)
        elif state_prison['Sex'] == 'Female':
            wiki_prison_df = wiki_prison_df.append({'State': state_prison['State'], 'Prison': state_prison['Prison'], 'Status': 'Operational (ABS)', 'Managed': 'Unknown', 'Public/Private': '?', 'Capacity': '?', 'Males': 0, 'Females': state_prison['Prisoners'], 'Latitude': 0, 'Longitude': 0}, ignore_index=True)

#Write scraped details to file
print(wiki_prison_df)

wiki_prison_df.to_csv('prison_list.csv', index=False, header=True)

