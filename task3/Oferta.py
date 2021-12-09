#!/usr/bin/env python
# coding: utf-8

# In[15]:


import datetime
import numpy as np
import  decimal 


# In[16]:


class Pojazd():
    
    def __init__(self, marka, model):
        self.marka = marka
        self.model = model
    
    def __str__(self):
        return f'{self.marka} {self.model}'


# In[17]:


class Element(Pojazd):
    
    def __init__(self,marka,model, kategoria, nazwaElemntu):
        super().__init__(marka, model)
        self.kategoria = kategoria
        self.nazwaElemntu = nazwaElemntu
    
    def __str__(self):
        return super().__str__()+" "+self.nazwaElemntu


# In[18]:


class Samochód(Pojazd):
    
    def __init__(self, marka, model, rocznik):
        super().__init__(marka,model)
        self._licznik = None
        self._paliwo = None
        self.rocznik = rocznik
    
    def stanLicznika(self, stanLicznika):
        self._licznik = stanLicznika
    
    def rodzajPaliwa(self, paliwo):
        self._paliwo = paliwo
    
    def wiek(self):
        now = datetime.datetime.now()
        return now.year - self.rocznik
    
    def __str__(self):
        if self._licznik is not None and self._paliwo is None:
            return super().__str__()+ f" wiek: {self.wiek()} lat {self._licznik} km"
        elif self._licznik is None and self._paliwo is not None:
            return super().__str__()+ f" wiek: {self.wiek()} lat {self._paliwo}"
        elif self._licznik is not None and self._paliwo is not None:
            return super().__str__()+ f" wiek: {self.wiek()} lat {self._licznik} km {self._paliwo}"
        else:
            return super().__str__()+ f" wiek: {self.wiek()} lat"


# In[96]:


class Oferta():
    def __init__(self, cena, *args):
        self._data = datetime.datetime.now()        
        self.cena = float(cena)
        self.elementyOferty = args
    
    def __str__(self):
        result = "{:.2f}".format(self.cena) + " zł"
        elementy = "".join(" + " + element.__str__() for element in self.elementyOferty )        
        return result + elementy[2:]