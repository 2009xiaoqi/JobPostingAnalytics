# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 10:57:04 2017

@author: JiLi
"""

# -*- coding: utf-8 -*-
import sys

"""
Created on Mon Aug 14 11:25:32 2017

@author: JiLi
"""

from bs4 import BeautifulSoup  # For HTML parsing
import urllib2  # Website connections
import re  # Regular expressions
from time import sleep  # To prevent overwhelming the server between connections
from collections import Counter  # Keep track of our term counts
from nltk.corpus import stopwords  # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd  # For converting results to a dataframe and bar chart plots %matplotlib inline
import requests
import bs4
import time
import json

import scraping_keywords

#Your desired keywords to analyze for frequency
technology_skills=["AI", "Blockchain", "Bots", "Cloud Platforms", "Cognitive Computing", "Computer Vision", "Conversational UI","Deep Learning",
        "DevOps", "Edge Intelligence","Edge Sensing", "Event Stream Processing", "IoT Platforms","Machine Learning","NLP","Predictive Analytics",
        "Real Time Computing","Robotic Process Automation","Serverless Architecture"]

#Your desired query URL from indeed.ca
# job_postings = scraping_functions.getURLs('/jobs?q=developer&l=toronto')
# jobs_dataframe = scraping_functions.scrapeJobs(job_postings)
# scraping_functions.analyzeJobs(skills,jobs_dataframe)

# with open("lobbying.json", "w") as writeJSON:
#    json.dump(lobbying, writeJSON)


# URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"
# conducting a request of the stated URL above:
# page = requests.get(URL)
# specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
# soup = BeautifulSoup(page.text, "html.parser")
# printing soup in a more structured tree format that makes for easier reading
# print(soup.prettify())


max_results_per_city = 100
city_set = ['New+York', 'Chicago', 'San+Francisco', 'Austin', 'Seattle', 'Los+Angeles', 'Philadelphia', 'Atlanta',
            'Dallas', 'Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']
columns = ["job_title","company_industry","key_words","company_name", "location", "summary", "time_posted", "salary", "url"]
#columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
sample_df = pd.DataFrame(columns=columns)
#for city in city_set:
for start in range(0, max_results_per_city, 10):
    #page = requests.get('https://www.indeed.com/jobs?q=executive+director&l=' + str(city) + '&start=' + str(start))
    page = requests.get('https://www.indeed.com/jobs?q=data+scientist&l=' + '&start=' + str(start))# page for executive and director
    #page = requests.get('https://www.indeed.com/jobs?q=scientist&l=' + '&start=' + str(start)) # page for scientist
    #page = requests.get('https://www.indeed.com/jobs?q=architect&l=' + '&start=' + str(start))  # page for architect
    #page = requests.get('https://www.indeed.com/jobs?q=senior+architect+engineer&l=' + str(start))  # page for architect engineer
    #page = requests.get('https://www.indeed.com/jobs?q=senior+manager&l=' + '&start=' + str(start))
    time.sleep(1)  # ensuring at least 1 second between page grabs
    soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        # specifying row num for index of job posting in dataframe
        num = (len(sample_df) + 1)
        # creating an empty list to hold the data for each posting
        job_post = []
        # append city name
        #job_post.append(city)
        # grabbing job title
        key_words = []
        for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
            job_post.append(a["title"])
            url = "https://www.indeed.com" + a["href"]
            if url != None:  # if company link exists, access it. Otherwise, skip.
                try:
                    page = requests.get(url)
                    # specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
                    soup = BeautifulSoup(page.text, "html.parser")
                    # grabbing company and industry info: get into a deep layer
                    temp = soup.find_all(name="span", attrs={"class":"summary"})
                    if temp.__len__() == 0:
                        job_post.append("No summary found")
                        job_post.append("No key words found")
                    else:
                        for b in soup.find_all(name="span", attrs={"class": "summary"}):
                            # job_post.append(b.text.strip()) # append the first <p> which is the companry info and industry info
                            try:
                                job_post.append(b.find('p').text.strip())
                                #print(b.find('p').text.strip())
                                print(b.text.strip())
                                print("------------------------------------------------------------")
                            except:
                                print(sys.exc_info())
                                job_post.append("No company information found")
                            try:
                                text = b.text.strip()
                                jsonString = scraping_keywords.convert_text_to_API_Format(text)
                                key_words = scraping_keywords.extract_keywords(jsonString)
                                job_post.append(key_words)
                            except:
                                job_post.append("No key words created")

                except:
                    job_post.append("Bad url to find company info")
                    job_post.append("Bad url to find key words")

            else:
                job_post.append("Url not found")
        company = div.find_all(name="span", attrs={"class": "company"})
        if len(company) > 0:
            for b in company:
                job_post.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class": "result-link-source"})
            for span in sec_try:
                job_post.append(span.text)
                # grabbing location name
        c = div.findAll('span', attrs={'class': 'location'})
        for span in c:
            job_post.append(span.text)
            # grabbing summary text
        d = div.findAll('span', attrs={'class': 'summary'})
        if(len(d)==0):
            job_post.append('No summary found')
        else:
            for span in d:
                job_post.append(span.text.strip())
        #grab posting time
        c = div.findAll('span', attrs={'class': 'date'})
        if (len(c) == 0):
            job_post.append('No date found')
        else:
            for s in c:
                job_post.append(s.text.strip())
            # grabbing salary
        try:
            job_post.append(div.find('nobr').text)
        except:
            try:
                div_two = div.find(name="div", attrs={"class": "sjcl"})
                div_three = div_two.find("div")
                job_post.append(div_three.text.strip())
            except:
                job_post.append("No salary found")
                # appending list of job post info to dataframe at index num
        if url != None:
            job_post.append(url)
        else:
            job_post.append("No url found")

        if scraping_keywords.compare_key_words(key_words):
            sample_df.loc[num] = job_post

# saving sample_df as a local csv file — define your own local path to save contents
sample_df.to_csv("tech_health_with_time.csv", encoding='utf-8')
# pathName = "C:\Users\JiLi\Desktop\JobPosting.csv"
# sample_df.to_csv(pathName)
#

