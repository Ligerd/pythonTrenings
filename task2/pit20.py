#!/usr/bin/env python
# coding: utf-8

# In[7]:


# In[2]:


def wyliczPodatek():
    doch=None
    fullpod=None 
    while True:
        źródło = input('Podaj źródło:')
        if źródło != '':
            if doch==None:
                kwotaPrzychodu=float(input('Podaj kwotę przychodu w zł:'))
                kwotaUzyskaniaPrzychodu = float(input('Podaj kwotę uzyskania przychodu w zł:'))

                doch = kwotaPrzychodu-kwotaUzyskaniaPrzychodu
                fullpod=calculatePodatek(doch)
            else:
                kwotaPrzychodu= float(input('Podaj kwotę przychodu w zł:'))
                kwotaUzyskaniaPrzychodu = float(input('Podaj kwotę uzyskania przychodu w zł:'))
                doch=doch+(kwotaPrzychodu-kwotaUzyskaniaPrzychodu)
                fullpod=calculatePodatek(doch)
        else:
            break
    print('Dochód:', round(doch,2),'zł', 'wyliczony podatek:', round(fullpod,2),'zł')


# In[5]:


def calculatePodatek(currentDoch):
    ZmPod=0
    podatek=0 
    
    if currentDoch<=8000:
        ZmPod=1360
    elif currentDoch<13000:
        ZmPod=1360-(834.88*(currentDoch-8000)/5000)
    elif doch<85528:
        ZmPod=525.12
    elif currentDoch<127000:
        ZmPod=525.12-(525.12*(currentDoch-85528)/41472)
    elif currentDoch>127000:
        ZmPod=0
        
    if currentDoch<=8000:
        podatek=0
    elif currentDoch<85528:
        podatek=(currentDoch*0.17)-ZmPod
    elif currentDoch<1000000:
        podatek=14539.76+(0.32*(currentDoch-85528))-ZmPod
    elif currentDoch>1000000:
        podatek=14539.76+(0.32*(currentDoch-85528))-ZmPod+(0.04*(currentDoch-1000000))
    
    return podatek


# In[ ]:

wyliczPodatek()



