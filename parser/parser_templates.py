# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 23:13:32 2022

@author: Sagi
"""

import requests
from bs4 import BeautifulSoup
import json

class Tutor():
    def __init__(self, name, courses=None):
        self.name = name
        if courses is not None:
            self.courses = courses
        else:
            self.courses = []
    
    def change_name(self, name):
        self.name = name
    
    def change_course(self, courses):
        self.courses = courses
    
    def __eq__(self, other):
        return self.name == other.name
    
    def __hash__(self):
        return hash(self.name)
    
    def __str__(self):
        result = self.name + "\n"
        
        if self.courses:
            result += self.courses + "\n"
        
        return result

class TutorWithPage(Tutor):
    def __init__(self, name, url, courses=None):
        self.name = name
        self.url = url
        if courses is not None:
            self.courses = courses
        else:
            self.courses = []
    
    def parse_page(self):
        print("Method not yet implemented")
    
    def __str__(self):
        result = self.name + "\n" + self.url + "\n"
        
        if self.courses:
            result += "\n" + self.courses
        
        return result

class Parser():
    def __init__(self, url=None, filename=None):
        self.url = url
        self.filename = filename
        self.parsed = dict()
        self.school = None
        
    def parse(self):
        print("method not yet implemented")

    def write_to_file(self):
        if len(self.parsed) == 0:
            self.parse()
        
        if self.school is None:
            print("ERROR: self.school must be initialized in the parse function")
            return
        
        with open("tutors.json", "r") as infile:
            data = json.load(infile)
    
        data[self.school] = self.parsed
        
        with open("tutors.json", "w") as outfile:
            outfile.write(json.dumps(data, indent=4))

class PageParser(Parser):
    def __init__(self, url):
        self.url = url
        self.__html = None
        self.parsed = dict()
        self.school = None
    
    def get_page(self):
        response = requests.get(self.url)
        self.__html = BeautifulSoup(response.content, "html.parser")
        
        return self.__html

class NestedPageParser(Parser):
    def __init__(self, root_url, extension):
        self.root_url = root_url
        self.extension = extension
        self.__html = None
        self.parsed = dict()
        self.school = None
    
    def get_page(self):
        response = requests.get(self.root_url + self.extension)
        self.__html = BeautifulSoup(response.content, "html.parser")
        
        return self.__html