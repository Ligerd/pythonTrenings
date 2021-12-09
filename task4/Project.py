#!/usr/bin/env python
# coding: utf-8

# # Założenia
# W tym rozdziale przedstawie ogólne załozenia projektowe.
# Na stronie MediaMarkt zjadowały się następujące parametry laptopów: Monitor, RAM, Dysk, GPU, System i Cena. Jednak na stronie Morele nie były podane dane o dysku oraz w niektórych laptopach, jak Apple, nie był podany układ graficzny oraz rozmiar dysku (była tylko możliwość wyboru rozwiaru dysku po kliknęciu w ten laptop). Więc przyjęłam takie założenia, że identifikuję laptopy według pełnej zgodności nazw i wielkości parametrów. 
# 

# In[23]:


from selenium import webdriver
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import re
from pyjarowinkler import distance


# In[2]:


def parseMediaMarktPage(driver,columns) -> list:
    full_object = driver.find_elements_by_xpath("//*[@class='m-offerBox_contentInner']")
    prices_objects = driver.find_elements_by_xpath("//*[@class='m-offerBox_pricing']")
    outPuts = [[] for i in range(len(columns))]
    for index in range(len(full_object)):
        title = parseTitleMediaMarkt(full_object[index])
        price = prices_objects[index].find_element_by_class_name("m-priceBox_price").text.split(',')[0]
        outPuts[0].append(title)
        outPuts[-1].append(price)
        ulBlock = full_object[index].find_element_by_class_name("b-ofr_boxDataItem.is-tech")
        liBlocks = ulBlock.find_elements_by_tag_name("li")
        if len(liBlocks)== 0 or len(liBlocks)!=len(columns[1:-1]):
            for index in range(1,len(columns)-1):
                outPuts[index].append(None)
        else:
            for indexli in range(0,len(liBlocks)):
                textOfLiBlock = liBlocks[indexli].find_element_by_tag_name("strong").get_attribute("innerHTML")
                outPuts[indexli+1].append(' '.join(textOfLiBlock.split()))
    return outPuts


# In[3]:


def parseTitleMediaMarkt(driver)->str:
    spliteteTitele = driver.find_element_by_tag_name('a').text.split('/')
    if spliteteTitele[0]=="Laptop":
        return " ".join(spliteteTitele[:2]).replace("Laptop", "", 1).strip()
    else:
        return "".join(spliteteTitele[:1]).replace("Laptop", "", 1).strip()


# In[39]:


def parseMediamarktPage():
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    url = "https://mediamarkt.pl/komputery-i-tablety/laptopy-laptopy-2-w-1/notebooki"
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    pagination = soup('span',{'class': "m-pagination_count"})[0].text.split()[1]
    column_names = ["Title",'Monitor', 'Processor', 'RAM', "Dysk","GPU","System", "Prices"]
    df = pd.DataFrame(columns = column_names)
    for i in range(1,int(pagination)+1):
        if i == 1:
            paramsofLaptops = parseMediaMarktPage(driver,column_names)
            df = df.append(pd.DataFrame(dict(zip(column_names, paramsofLaptops))), ignore_index = True)
        else:
            driver.get(url+ "?page="+str(i))
            paramsofLaptops = parseMediaMarktPage(driver,column_names)
            df = df.append(pd.DataFrame(dict(zip(column_names, paramsofLaptops))), ignore_index = True)
    df = df.sort_values('Title').reset_index(drop=True)
    df.to_csv("MediaMarkt_Laptops.csv")
    driver.quit()
    return df


# In[6]:


dff = parseMediamarktPage()


# # MORELE

# In[7]:


def getNumberOfPagesMorele(driver) -> int: 
    numbrOfPagesStr= driver.find_element_by_class_name('pagination-btn-nolink-anchor').text
    return int(numbrOfPagesStr)


# In[8]:


def getPropertiesOfLaptops(driver) -> list: 
    return driver.find_elements_by_class_name("cat-product-features")


# In[37]:


def getPricesOfLaptops(driver) -> list:
    pricesDiv = driver.find_elements_by_class_name("price-new")
    regexExp = "[^\d\,]"
    prices = []
    for price in pricesDiv:
        clearPrice = re.sub(regexExp,"",price.text).replace(',',".")
        prices.append(float(clearPrice))
    return prices
        


# In[40]:


def parceProperties(laptopInformationDiv, columns) -> list:
    outPuts = [[] for i in range(len(columns[:-1]))]
    for divPropertiesOfLaptop in laptopInformationDiv:
        propertiesOfLaptop = divPropertiesOfLaptop.find_elements_by_class_name("cat-product-feature")
        outPuts[0].append(getTitleOfLaptopOnPage(divPropertiesOfLaptop))
        for propertyIndex in range(1,len(outPuts)) :
            if len(propertiesOfLaptop)== 5:
                outPuts[propertyIndex].append(propertiesOfLaptop[propertyIndex-1].get_attribute("title"))
            else:
                outPuts[propertyIndex].append(None)
    return outPuts


# In[41]:


def getTitlesOfLaptopsOnPage(driver) -> list:
    return [ title.text.split('(')[0][:-1]  for title in driver.find_elements_by_xpath("//*[@class='cat-product-name']/a")]


# In[42]:


def getTitleOfLaptopOnPage(driver):
    return driver.find_element_by_class_name("productLink").text.split("/")[0].replace("Laptop ","",1)


# In[13]:


def getLaptopInformationDiv(driver)-> list:
    return driver.find_elements_by_class_name("cat-product-center-inside")


# In[43]:


def parseMorelo():
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    url = "https://www.morele.net/kategoria/laptopy-31/"
    driver.get(url)
    pagination = getNumberOfPagesMorele(driver)
    column_names = ["Title",'GPU', 'RAM', "Processor","Monitor","System", "Prices"]
    df = pd.DataFrame(columns = column_names)
    for i in range(1,int(pagination)):
        if i == 1:
            prices = getPricesOfLaptops(driver)
            paramsofLaptops = parceProperties(getLaptopInformationDiv(driver),column_names)
            paramsofLaptops = paramsofLaptops + [prices]
            df = df.append(pd.DataFrame(dict(zip(column_names, paramsofLaptops))), ignore_index = True)
        else:
            driver.get(url+ ",,,,,,,,0,,,,/"+str(i)+"/")
            prices = getPricesOfLaptops(driver)
            paramsofLaptops = parceProperties(getLaptopInformationDiv(driver),column_names)
            paramsofLaptops = paramsofLaptops + [prices]
            df = df.append(pd.DataFrame(dict(zip(column_names, paramsofLaptops))), ignore_index = True)
    df = df.sort_values('Title').reset_index(drop=True)
    df.to_csv("Morelo_Laptops.csv")
    driver.quit()
    return df


# In[24]:


morelo = parseMorelo()


# # Find similarity

# In[5]:


mediaMarkt = pd.read_csv('MediaMarkt_Laptops.csv',index_col=0)
morelo = pd.read_csv('Morelo_Laptops.csv',index_col=0)


# In[15]:


def identifySameLaptops(baseDf, targetDf,similarity):
    sameLaptoptBase = pd.DataFrame(columns=baseDf.columns)
    sameLaptoptTarge = pd.DataFrame(columns=targetDf.columns)
    for index, rowbaseDf in baseDf.iterrows():
        brand = extractLaptopBrand(rowbaseDf.Title)
        laptopsForBrand= targetDf[targetDf['Title'].str.contains(brand,case=False)]        
        for indexTarget, rowTargetDf in laptopsForBrand.iterrows():
            titleSimilarity = distance.get_jaro_distance(rowbaseDf.Title,rowTargetDf.Title, winkler=True, scaling=0.1)
            if titleSimilarity>similarity:
                if compareParams(rowbaseDf,rowTargetDf):
                    sameLaptoptBase = sameLaptoptBase.append(pd.DataFrame([rowbaseDf]))
                    sameLaptoptTarge = sameLaptoptTarge.append(pd.DataFrame([rowTargetDf]))
    dfOut = concateResultIndentifycation(sameLaptoptBase, sameLaptoptTarge)
#     sameLaptoptBase = sameLaptoptBase.drop_duplicates('Title')
    sameLaptoptBase.to_csv("IdentifyMediaMarkt.csv")
    sameLaptoptTarge.to_csv("IdentifyMorele.csv")
    dfOut.to_csv("LaptopIdentification.csv")
    return dfOut


# In[7]:


def concateResultIndentifycation(base, target):
    base.rename(columns = {"Prices": "PriceMediaMarkt"}, inplace = True)
    base = base.reset_index(drop=True)
    target = target.reset_index(drop=True)
    base['PriceMorele'] = target["Prices"]
#     return base.sort_values('PriceMorele', ascending=True).drop_duplicates('Title').sort_index().reset_index(drop=True)
    return base


# In[8]:


def extractLaptopBrand(title:str)->str:
    titleList = title.split()
    if titleList[0]=="2w1":
        return titleList[1]
    else:
        return titleList[0]


# In[22]:


def prepareProcFormat(proc:str)->str:
    return re.sub('[™®]', '', proc)


# In[10]:


def prepareGPUFormat(gpu:str)->str:
    notAllowdWords = ["Laptop","GPU"]
    for notAllowdWord in notAllowdWords:
        gpu = gpu.replace(notAllowdWord, '')
    return gpu.strip()


# In[18]:


def compareGpu(baseGpu:str, targetGpu:str)->bool:
#     if baseGpu == "Brak" or targetGpu == "Brak":
#         return True
#     else:
    return prepareGPUFormat(targetGpu) in baseGpu

def compareRAM(baseRAM:str, targetRAM:str)->bool:
    return targetRAM in baseRAM

def compareMonitor(baseMonitor:str , targetMonitor:str)->bool:
    return targetMonitor in baseMonitor

def compareSystem(baseSys:str,targetSys:str)->bool:
    return targetSys in baseSys

def compareProcessors(baseProc:str, TargetProc:str)->bool:
    return TargetProc in baseProc


# In[19]:


def compareParams(base, target)->bool:
    if compareProcessors(prepareProcFormat(base.Processor),target.Processor):
        if compareGpu(base.GPU,target.GPU):
            if compareRAM(base.RAM, target.RAM):
                if compareMonitor(base.Monitor, target.Monitor):
                    if compareSystem(base.System, target.System):
                        return True
                    else: 
                        return False
                else:
                    return False
            else:
                return False
        else: 
            return False
    else:
        return False


# In[25]:


itdentify=identifySameLaptops(mediaMarkt,morelo,0.90)


# In[26]:


itdentify


# In[ ]:




