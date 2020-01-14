# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 04:10:59 2020

@author: sicTa
"""

class Word:
    def __init__(self, array, name):
        self.array = array
        self.name = name
        
        
    def return_name(self):
        return self.name
    
    def return_array(self):
        return self.array