# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 14:53:43 2018

@author: PeerapongE
"""

import func_scrap_hipflat
import pickle
import os
import time

import openpyxl
from openpyxl import Workbook

#Getting back the objects:

start_time = time.time()

with open('objs.pkl','rb') as f:  # Python 3: open(..., 'rb')
    (CONDO_NAME, CONDO_AREA, CONDO_URL) = pickle.load(f)

dest_filename = 'hipflat_data.xlsx'

try: # Delete the old file if exist
    os.remove(dest_filename)
except OSError:
    print('[PeerapongE]: File does not exist')
    pass


wb = Workbook()
ws1 = wb.active
ws1.title = "Condo_detail_info"

# 1-Header info
ws1['A1'] = 'Condo_NAME'
ws1['B1'] = 'Address'
ws1['C1'] = 'Year_built'
ws1['D1'] = 'Area_m2'
ws1['E1'] = '#_Tower' 
ws1['F1'] = '#_Floor'
# 2-Market value 
ws1['G1'] = 'Sale_Price'
ws1['H1'] = 'Sale_Price_Increment[Quarter]'
ws1['I1'] = 'Sale_Price_Increment[Year]'
ws1['J1'] = 'Rental_Yield'
ws1['K1'] = 'Rental_Yield_Increment[Year]'
# 3-Transportation: Distance to Pahonyothin MRT
ws1['L1'] = 'Distance to Pahonyothin MRT'
# 4-lat long location
ws1['M1'] = 'Latitude'
ws1['N1'] = 'Longtitude'

wb.save(filename = dest_filename)
""" Main Scraping loop """
for j in range(1138,len(CONDO_URL)) :
#for j in range(1138,1139) :
    print('[PeerapongE]: Current j = ' + str(j))
    #quote_page = 'https://www.hipflat.com/projects/abstracts-phahonyothin-park-adfwjs' #Abstracts
    quote_page = CONDO_URL[j]
    
    (HD_NAME, HD_LOC, HD_YB, HD_AR, HD_NT, HD_FL,
     MK_VAL, MK_VALIQ, MK_VALIY, MK_RENT, MK_RENTIY,
     TP_DIST_CLP_VAL,
     LATITUDE,LONGTITUDE) = func_scrap_hipflat.scrap_hipflat(quote_page)

    """ Printing info """

    # 1-Header info
    ws1['A'+str(j+2)] = HD_NAME.strip().split('\x03')[0]
    ws1['B'+str(j+2)] = HD_LOC
    ws1['C'+str(j+2)] = HD_YB
    ws1['D'+str(j+2)] = HD_AR
    ws1['E'+str(j+2)] = HD_NT
    ws1['F'+str(j+2)] = HD_FL
    # 2-Market value 
    ws1['G'+str(j+2)] = MK_VAL
    ws1['H'+str(j+2)] = MK_VALIQ
    ws1['I'+str(j+2)] = MK_VALIY
    ws1['J'+str(j+2)] = MK_RENT
    ws1['K'+str(j+2)] = MK_RENTIY
    # 3-Transportation: Distance to Pahonyothin MRT
    ws1['L'+str(j+2)] = TP_DIST_CLP_VAL
    # 4-lat long location
    ws1['M'+str(j+2)] = LATITUDE
    ws1['N'+str(j+2)] = LONGTITUDE

    wb.save(filename = dest_filename)
    time.sleep(1)
    print('[PeerapongE]: Complete Web hipflat info Striping from condo : ' + HD_NAME)
    print('[PeerapongE]: Elapse time = ' + str(time.time() - start_time) + ' seconds')
    

    

print('[PeerapongE]: Complete Web hipflat info Striping')
print('[PeerapongE]: Total time = ' + str(time.time() - start_time) + ' seconds')