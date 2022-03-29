# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 23:13:32 2022

@author: Sagi
"""

import requests
from bs4 import BeautifulSoup

class Tutor():
    def __init__(self, name, courses=None):
        self.name = name
        self.courses = courses
    
    def change_name(self, name):
        self.name = name
    
    def change_course(self, courses):
        self.courses = courses
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        return self.name

class TutorWithPage(Tutor):
    def __init__(self, name, url, courses=None):
        self.name = name
        self.url = url
        self.courses = courses
    
    def __str__(self):
        return self.name + "\n" + self.url

class Parser():
    def __init__(self, url=None, filename=None):
        self.url = url
        self.filename = filename
        
    def parse(self):
        print("method not yet implemented")

class PageParser(Parser):
    def __init__(self, url=None):
        self.url = url
        self.__html = None
    
    def get_page(self):
        response = requests.get(self.url)
        self.__html = BeautifulSoup(response.content, "html.parser")
        
        return self.__html

class UConnParser(PageParser):
    def parse(self):
        page = self.get_page()
        
        table = page.find("table", {"class": "main_schedule_table"})
        
        tutor_hrefs = table.find_all("a", {"class": "qc_super"})
        
        tutors = set()
        
        for href in tutor_hrefs:
            tutors.add(TutorWithPage(href.text, href['href']))
        
        return tutors

if __name__ == "__main__":
    parser = UConnParser("https://qcenter.uits.uconn.edu/public/schedule")
    
    tutors = parser.parse()
    for tutor in tutors:
        print(tutor)