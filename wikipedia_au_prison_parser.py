from lxml import html
import requests
import csv
import re

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


base_url = 'https://en.wikipedia.org'

page = requests.get(base_url + '/wiki/List_of_prisons_in_Australia')
html_content = html.fromstring(page.content)
html_content = html.make_links_absolute(html_content, base_url, False)

prison_tables = html_content.xpath('//div[@id="mw-content-text"]/div/table', smart_strings=False)

prison_list = []
prison_details = ['State', 'Prison', 'Status', 'Capacity', 'Latitude', 'Longitude']
prison_list.append(prison_details)
prison_column = 0
status_column = 1
capacity_column = 6
location_column = 7

state = ''
row_count = 0

for state_prisons in prison_tables:
    prisons = state_prisons.xpath('./tbody/tr', smart_strings=False)

    prison = ''
    status = ''
    capacity = ''
    location = ''
    for row in prisons:
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
            row_count += 1
        elif (len(row) == 7 or len(row) == 8) and row_count > 1:
            prison_lat = 0
            prison_lon = 0

            if len(row) == 7:
                column_offset = -1
            elif len(row) == 8:
                column_offset = 0

            print('')
            print('Prison')
            prison = row[prison_column]
            prison_name = prison.text_content().strip().rstrip('[0123456789]')
            print(prison_name)
            for prison_elements in prison:
                prison_attributes = prison_elements.items()
                for attr in prison_attributes:
                    if attr[0] == 'href':
                        print('href: ' + attr[1])
                        href = attr[1]
                        prison_page = requests.get(href)
                        prison_html_content = html.fromstring(prison_page.content)

                        prison_geodec = []
                        prison_geodec_span = prison_html_content.xpath('//span[@class="geo-dec"]/text()')
                        if len(prison_geodec_span) > 0:
                            prison_geodec = prison_geodec_span[0].split(' ')
                            if len(prison_geodec) > 0:
                                prison_lat = signdec(prison_geodec[0])
                                prison_lon = signdec(prison_geodec[1])
                            elif len(prison_geodec) == 0:
                                prison_lat = dms2dec(prison_html_content.xpath('//span[@class="latitude"]/text()')[0].split(' '))
                                prison_lon = dms2dec(prison_html_content.xpath('//span[@class="longiture"]/text()')[0].split(' '))
            
            print('Status')
            status = row[status_column].text_content().strip().rstrip('[0123456789]')
            print(status)
            print('Capacity')
            capacity = row[capacity_column + column_offset].text_content().strip()
            print(capacity)
            print('Location')
            location = row[location_column + column_offset]
            print(location.text_content().strip().rstrip('[0123456789]'))
            if prison_lat == 0 and prison_lon == 0:
                for location_elements in location:
                    location_attributes = location_elements.items()
                    for attr in location_attributes:
                        if attr[0] == 'href':
                            print('href: ' + attr[1])
                            href = attr[1]
                            
                            location_page = requests.get(href)
                            location_html_content = html.fromstring(location_page.content)
                            
                            prison_geodec = []
                            prison_geodec_span = location_html_content.xpath('//span[@class="geo-dec"]/text()')
                            if len(prison_geodec_span) > 0:                            
                                prison_geodec = prison_geodec_span[0].split(' ')
                                if len(prison_geodec) > 0:
                                    prison_lat = signdec(prison_geodec[0])
                                    prison_lon = signdec(prison_geodec[1])
                                if len(prison_geodec) == 0:
                                    prison_lat = dms2dec(prison_html_content.xpath('//span[@class="latitude"]/text()')[0].split(' '))
                                    prison_lon = dms2dec(prison_html_content.xpath('//span[@class="longiture"]/text()')[0].split(' '))
            print('Prison Latitude: ' + str(prison_lat))
            print('Prison Longitude: ' + str(prison_lon))

            prison_details = [state, prison_name, status, capacity, prison_lat, prison_lon]
            prison_list.append(prison_details)

            row_count += 1

with open('prison_list.csv', 'w', newline='', encoding='utf-8') as csv_prison_file:
    csvwriter = csv.writer(csv_prison_file, dialect='excel')
    csvwriter.writerows(prison_list)

