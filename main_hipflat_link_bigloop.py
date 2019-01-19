# -*- coding: utf-8 -*-
"""
Created on Sun Dec 31 13:05:29 2017

For stipping web link

@author: PeerapongE
"""

import urllib
from bs4 import BeautifulSoup

#import csv

import pickle
import os

import openpyxl
from openpyxl import Workbook
from openpyxl.compat import range

import time

#quote_page = 'https://www.hipflat.co.th/en/market/condo-chatuchak-mwxhss'

quote_page = 'https://www.hipflat.com/market/condo-bangkok-skik'
page = urllib.request.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')

print('[PeerapongE] : Start Extract and Print all links')

"""
-------------------Step-1-- Extracting link data -------------------
"""


AREA_OBJ = soup.find('ul', class_='directories__lists-all')

all_area_link = AREA_OBJ.find_all("a")

AREA_URL = []
AREA_NAME = []
CONDO_URL = []
CONDO_NAME = []
CONDO_AREA = []

i = 0

url_main = 'https://www.hipflat.co.th'

for area_link in all_area_link:
    area_linki = (area_link.get("href"))
    area_full_linki = url_main + area_linki
    area_name = area_link.text.strip().split('\n')[0].strip()
    AREA_NAME.append(area_name)
    AREA_URL.append(area_full_linki )
    
    print('[PeerapongE] : Working on : ' + area_link.text + ' area --> looping' )
    quote_condo_page = area_full_linki
    page_condo = urllib.request.urlopen(quote_condo_page) 
    soup_condo = BeautifulSoup(page_condo, 'html.parser')
    CONDO_OBJ = soup_condo.find('ul', class_='directories__lists-all')

    all_condo_link = CONDO_OBJ.find_all("a")
    for condo_link in all_condo_link:
        condo_linki = (condo_link.get("href"))
        condo_full_linki = url_main + condo_linki 
        
        CONDO_NAME.append(condo_link.text.strip())
        CONDO_AREA.append(area_name)
        CONDO_URL.append(condo_full_linki )
        
        
    j = 0    
    
"""
-------------------Step-2-- Writing data -------------------
"""
#
dest_filename = 'hipflat_link.xlsx'

try:
    os.remove(dest_filename)
except OSError:
    print('[PeerapongE]: File does not exist')
    pass

wb = Workbook()
ws1 = wb.active
ws1.title = "condo_name_link"

ws1['A1'] = 'Condo_name'
ws1['B1'] = 'Condo_area'
ws1['C1'] = 'Condo_link'


for i in range(0,len(CONDO_URL)):
    ws1['A'+str(i+2)] = CONDO_NAME[i].strip().split('\x03')[0] # for some bad name condo 317
    ws1['B'+str(i+2)] = CONDO_AREA[i]
    ws1['C'+str(i+2)] = CONDO_URL[i]
    
wb.save(filename = dest_filename)
#
#"""
#-------------------Step-3-- Save Variable as pickle -------------------
#"""
#
# Saving the objects:    
with open('objs.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
    pickle.dump([CONDO_NAME, CONDO_AREA, CONDO_URL], f)

## Getting back the objects:
#with open('objs.pkl','rb') as f:  # Python 3: open(..., 'rb')
#    CONDO_NAME, CONDO_URL = pickle.load(f)
       
print('[PeerapongE] : Complete Program')
