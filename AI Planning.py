# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:16:34 2020

@author: Rahul
"""
#This is a program for the ID1214 Lab2 problem based on 
# the Tower Of Hanoi Problem

def Lab2(n,from_floor,to_floor,intermediate_floor):
    if n == 1:
        print("Moved Box 1 from",from_floor,"to",to_floor)
        return
    Lab2(n-1,from_floor,intermediate_floor,to_floor)
    print("Move Box",n,"from",from_floor,"to",to_floor)
    Lab2(n-1,intermediate_floor,to_floor,from_floor)
    
if __name__ == "__main__":
    n = 3
    Lab2(n,'A','C','B')
    
    
    
    