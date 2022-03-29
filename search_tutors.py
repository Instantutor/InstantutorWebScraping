# -*- coding: utf-8 -*-
"""
Created on Wed Mar 23 14:59:16 2022

Data from the following api:
    https://www.back4app.com/database/back4app/list-of-all-us-colleges-and-universities/get-started/python/rest-api/requests?objectClassSlug=university-dataset-api

@author: Sagi
"""

import json
import re
import requests
from bs4 import BeautifulSoup
from googlesearch import search

NUM_RESULTS = 3
TEST_UNIS = ["Northeastern", "Rpi", "Rit"]
SEARCH_STRING = " Academic Support Center"

def get_universities():
    url = 'https://parseapi.back4app.com/classes/University?limit=10000'
    headers = {
        'X-Parse-Application-Id': 'Ipq7xXxHYGxtAtrDgCvG0hrzriHKdOsnnapEgcbe', # This is the fake app's application id
        'X-Parse-Master-Key': 'HNodr26mkits5ibQx2rIi0GR9pVCwOSEAkqJjgVp' # This is the fake app's readonly master key
    }
    data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
    
    universities = [obj['name'] for obj in data['results']]
    
    return universities

def get_valid_websites(unis):
    query = SEARCH_STRING
    
    valid_websites = {}

    uni_counter = 0

    for uni in unis:
        valid_urls = []
        
        for url in search(uni + query, num=NUM_RESULTS, stop=NUM_RESULTS, pause=2):
            # Skip pdfs
            if (re.search(".pdf$", url)):
                continue
            # Actual parse
            try:
                response = requests.get(url, timeout=10)
                html = BeautifulSoup(response.content, "html.parser")
                if (re.search('tutor', html.body.text, re.IGNORECASE)):
                    valid_urls.append(url)
            except Exception as e:
                print("Exception:", e)

        valid_websites.update({uni : valid_urls})

        # Print for sanity
        uni_counter += 1
        print('{:3d}'.format(uni_counter) + ":", uni)
    return valid_websites

def update_json_valid_links(unis):
    valid_websites = get_valid_websites(unis)
    
    with open("temp_tutoring_websites.json", "r") as infile:
        data = json.load(infile)
    
    data.update(valid_websites)
    
    with open("temp_tutoring_websites.json", "w") as outfile:
        outfile.write(json.dumps(data, indent=4))

# Laguardia causes problems collect around it
def batch_write_to_file(batch_size, start=None):
    unis = get_universities()
    
    if (start):
        if (start >= len(unis)):
            return
        test_range = range(start//batch_size, len(unis)//batch_size)
    else:
        test_range = range(len(unis)//batch_size)
    
    for i in test_range:
        print("Batch:", "{0}-{1}".format(i*batch_size, (i+1)*batch_size))
        update_json_valid_links(unis[i*batch_size:(i+1)*batch_size])
    
    final_batch_start = len(unis) - len(unis) % batch_size
    print("Batch:", "{0}-{1}".format(final_batch_start, len(unis)))
    update_json_valid_links(unis[final_batch_start:len(unis)])

if __name__ == "__main__":
    #unis = get_universities()
    #batch_write_to_file(100, 3200)
    #https://poorvucenter.yale.edu/dropin-residential-college-stem-tutors
    #https://qcenter.uits.uconn.edu/public/schedule
    #https://info.rpi.edu/advising-learning-assistance/learning-assistants

    with open("temp_tutoring_websites.json", "r") as infile:
        data = json.load(infile)
        
    
    counter = 0
    new_data = {}
    for key in data:
        valid_urls = []
        counter += 1
        for url in data[key]:
            try:
                response = requests.get(url, timeout=10)
                html = BeautifulSoup(response.content, "html.parser")
                if (re.search('drop in', html.body.text, re.IGNORECASE)
                    or re.search('drop-in', html.body.text, re.IGNORECASE)
                    or re.search('schedule', html.body.text, re.IGNORECASE)):
                    valid_urls.append(url)
                    print("found")
            except Exception as e:
                print("Exception:", e)
        if (len(valid_urls) > 0):
            new_data[key] = valid_urls
        print('{:4d}:'.format(counter), key)

    with open("query_result_websites.json", "w") as outfile:
        outfile.write(json.dumps(new_data, indent=4))