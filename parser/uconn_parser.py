import requests
from bs4 import BeautifulSoup
import json

from parser_templates import TutorWithPage, NestedPageParser

class UConnTutor(TutorWithPage):
    def parse_page(self):
        response = requests.get(self.url)
        html = BeautifulSoup(response.content, "html.parser")
        
        description = html.find("div", {"class": "detailsname"})

        lines = str(description.prettify()).splitlines()
        
        line_ctr = 0
        line_len = len(lines)
        
        while (line_ctr < line_len):
            if lines[line_ctr].find("</h3>") != -1:
                line_ctr += 1
                self.year = lines[line_ctr].strip()
            if lines[line_ctr].find("Primary") != -1:
                line_ctr += 2
                self.primary = lines[line_ctr].strip()
            if lines[line_ctr].find("Secondary") != -1:
                line_ctr += 2
                self.secondary = lines[line_ctr].strip()
            if lines[line_ctr].find("Major") != -1:
                line_ctr += 2
                self.majors = []
                majors = lines[line_ctr].strip().replace(":", "").split(",")
                for major in majors:
                    self.majors.append(major.strip())
            
            line_ctr += 1
        
        self.schedule = dict()
        
        for li in description.findAll("li"):
            lines = li.text.splitlines()
            day = lines[0].replace(":", "").strip()
            self.schedule[day] = []
            for line in lines[1:len(lines)-1]:
                self.schedule[day].append(line.strip())
        
        for course in html.body.findAll("h5"): 
            self.courses.append(course.text.strip())

class UConnParser(NestedPageParser):
    def parse(self):
        self.school = "UCONN"
        
        page = self.get_page()
        table = page.find("table", {"class": "main_schedule_table"})
        tutor_hrefs = table.find_all("a")
        
        for a in tutor_hrefs:
            self.parsed[a.text] = UConnTutor(a.text, self.root_url + a['href'])
            
        for key in self.parsed:
            print(key)
            self.parsed[key].parse_page()

        for key in self.parsed:
            new_val = self.parsed[key].__dict__
            new_val.pop("name")
            new_val.pop("url")
            self.parsed[key] = new_val
        
        return self.parsed

if __name__ == "__main__":
    parser = UConnParser("https://qcenter.uits.uconn.edu", "/public/schedule")
    
    #tutors = parser.parse()
    parser.write_to_file()

    '''
    tutor = UConnTutor("test", "https://qcenter.uits.uconn.edu/public/people/person/id_971")
    tutor.parse_page()
    js = tutor.__dict__
    js.pop("url")
    print(js)
    '''
    