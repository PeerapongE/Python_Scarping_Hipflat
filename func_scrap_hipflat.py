# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 12:24:54 2017

@author: PeerapongE
"""
def scrap_hipflat(quote_page):

    import urllib
    from bs4 import BeautifulSoup
    import re

    


    """
    -------------------Step-2-- Get html data -------------------
    """

    #quote_page = 'https://www.hipflat.com/projects/abstracts-phahonyothin-park-adfwjs' #Abstracts
    #quote_page = 'https://www.hipflat.co.th/en/projects/sym-vibhaladprao-ohjvej' #SYM Vipha
    #quote_page = 'https://www.hipflat.co.th/en/projects/ngamwadee-place-vjeyjg' #Ngamwadee (missing data test)
    #
    #

    #for index in range(0,len(CONDO_URL)):
    #    print('[PeerapongE]: Current url index is = ' + str(index))
    #    print(CONDO_URL[index])
    #
    #    quote_page = CONDO_URL[index]
    #    print('[PeerapongE]: Current working url = ' + quote_page)
    

    
    page = urllib.request.urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')




    """
    -------------------Step-2-- Extracting detail data from html -------------------
    """

    #print('Name = '+ name)

    #name_box2 = soup.find('div', attrs={'class': 'project-header-icons'})

    # find sub information in project-header-floor
    HD_NAME = []
    HD_LOC = []
    HD_YB = []
    HD_AR = []
    HD_NT = []
    HD_FL = []

    ########################################### Group-1: Header data (HD) ###########################################

    try: HD_NAME = soup.find('div', attrs={'class': 'project-header-name'}) .text.strip() # Condo name
    except: HD_NAME = ''

    try : HD_LOC = soup.find('span', attrs={'itemprop': 'streetAddress'}).text.strip() # Condo location
    except: HD_LOC = ''

    try : HD_YB = soup.find('li', attrs={'class': 'project-header-year'}).text.strip().split()[0] #Condo Year built
    except: HD_YB = ''

    try : HD_AR = soup.find('li', attrs={'class': 'project-header-area'}).text.strip().split()[0]  #Condo Area
    except: HD_AR = ''

    try : HD_NT = soup.find('li', attrs={'class': 'project-header-tower'}).text.strip().split()[0] #Condo N# Tower
    except: HD_NT = ''

    try : HD_FL = soup.find('li', attrs={'class': 'project-header-floor'}).text.strip().split()[0] #Condo N# Floor
    except: HD_FL  = ''

    ########################################### Group-2: Market (MK) value ###########################################
    MK_VAL    = []
    MK_VALIQ  = []
    MK_VALIY  = []
    MK_RENT   = []
    MK_RENTIY = []

    MK_TABLE = soup.find('ul', class_='market-data')
    MK_DATA = []

    try:
        for row in MK_TABLE.findAll('li'):
            datai = row.find('div', attrs={'class': 'indicator__amount'}).text.strip().split()[0]
            MK_DATA.append(datai)

        MK_VAL    = MK_DATA[0]    
        MK_VALIQ  = MK_DATA[1]
        MK_VALIY  = MK_DATA[2]
        MK_RENT   = MK_DATA[3]
        MK_RENTIY = MK_DATA[4]
    except:
        MK_VAL    = ''
        MK_VALIQ  = ''
        MK_VALIY  = ''
        MK_RENT   = ''
        MK_RENTIY = ''

    ########################################### Group-3: Transportation (TP) ###########################################

    TP_TABLE = soup.find('div', class_='neighborhood-destinations-wrapper neighborhood-destinations-wrapper--with-right-border')
    TP_PLACE = []
    TP_DIST = []
    TP_TIME = []
    TP_DIST_CLP = ''
    TP_TIME_CLP = ''
    TP_DIST_CLP_VAL = ''
    
    #for row in TP_TABLE.findAll(['small','h4']): #small = distance, time, h4 = location
    for row in TP_TABLE.findAll('h4'): #small, h4
        TP_PLACE.append(row.text)

    i = 0


    for row in TP_TABLE.findAll('small'): #small, h4
        DISTi = row.text.strip().split('/')[0]
        TIMEi = row.text.strip().split('/')[1]
        TP_DIST.append(DISTi)
        TP_TIME.append(TIMEi)
        if TP_PLACE[i] == 'Phahon Yothin':
            #Time value
            TP_DIST_CLP_UNIT = DISTi.split()[1]
            if TP_DIST_CLP_UNIT == 'km':
                TP_DIST_CLP_VAL = float(DISTi.split()[0]) * 1000
            else:
                TP_DIST_CLP_VAL = float(DISTi.split()[0])
            #
            TP_TIME_CLP = TIMEi
        i = i + 1

    ########################################### Group-4: Lat-Long location  ###########################################
    
    
    data_article = soup.find('article', class_='project')
    data_script = data_article.findAll('script')

    for data in data_script:

        script_i = data.string.strip().split('\n') #separate to list of multiple lines
    
        if script_i[0] == 'var initNeighborhood;': # If the data has first line as this one

            for line in script_i:

                if (line.strip()[0:4]) == 'lat:':
                    LATITUDE = re.split(':|,| ',line.strip())[2]
                elif (line.strip()[0:4]) == 'lng:':
                    LONGTITUDE = re.split(':|,| ',line.strip())[2]
    
    
    return (HD_NAME, HD_LOC, HD_YB, HD_AR, HD_NT, HD_FL,
            MK_VAL, MK_VALIQ, MK_VALIY, MK_RENT, MK_RENTIY,
            TP_DIST_CLP_VAL,
            LATITUDE,LONGTITUDE)
"""


-------------------Step-3-- Printing data to EXCEL -------------------
"""
#
#dest_filename = 'hipflat_scrap_info.xlsx'
#
#try:
#    os.remove(dest_filename)
#except OSError:
#    print('[PeerapongE]: File does not exist')
#    pass
#
#wb = Workbook()
#ws1 = wb.active
#ws1.title = "Condo_detail_info"
#
##ws1['A1'] = 'Condo_name'
##ws1['B1'] = 'url_link'
##for i in range(0,len(CONDO_URL)):
#i = 2
#
##MK_RENT = None
#
## 1-Header info
#ws1['A'+str(i)] = HD_NAME
#ws1['B'+str(i)] = HD_LOC
#ws1['C'+str(i)] = HD_YB
#ws1['D'+str(i)] = HD_AR
#ws1['E'+str(i)] = HD_NT
#ws1['F'+str(i)] = HD_FL
## 2-Market value 
#ws1['G'+str(i)] = MK_VAL
#ws1['H'+str(i)] = MK_VALIQ
#ws1['I'+str(i)] = MK_VALIY
#ws1['J'+str(i)] = MK_RENT
#ws1['K'+str(i)] = MK_RENTIY
## 3-Transportation: Distance to Pahonyothin MRT
#ws1['L'+str(i)] = TP_DIST_CLP_VAL
## 4-lat long location
#ws1['M'+str(i)] = LATITUDE
#ws1['N'+str(i)] = LONGTITUDE
#
#
## Topline definition
## 1-Header info
#ws1['A1'] = 'Condo_NAME'
#ws1['B1'] = 'Address'
#ws1['C1'] = 'Year_built'
#ws1['D1'] = 'Area_m2'
#ws1['E1'] = '#_Tower'
#ws1['F1'] = '#_Floor'
## 2-Market value 
#ws1['G1'] = 'Sale_Price'
#ws1['H1'] = 'Sale_Price_Increment[Quarter]'
#ws1['I1'] = 'Sale_Price_Increment[Year]'
#ws1['J1'] = 'Rental_Yield'
#ws1['K1'] = 'Rental_Yield_Increment[Year]'
## 3-Transportation: Distance to Pahonyothin MRT
#ws1['L1'] = 'Distance to Pahonyothin MRT'
## 4-lat long location
#ws1['M1'] = 'Latitude'
#ws1['N1'] = 'Longtitude'
#
#wb.save(filename = dest_filename)
#
#
#print('[PeerapongE]: Complete Web hipflat info Striping')