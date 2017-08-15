# -*- coding: utf-8 -*-
"""
Created on Mon Aug 14 11:25:32 2017

@author: JiLi
"""

from bs4 import BeautifulSoup # For HTML parsing
import urllib2 # Website connections
import re # Regular expressions
from time import sleep # To prevent overwhelming the server between connections
from collections import Counter # Keep track of our term counts
from nltk.corpus import stopwords # Filter out stopwords, such as 'the', 'or', 'and'
import pandas as pd # For converting results to a dataframe and bar chart plots %matplotlib inline
import requests
import bs4
import time
import json

#with open("lobbying.json", "w") as writeJSON:
#    json.dump(lobbying, writeJSON)


URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start=10"
#conducting a request of the stated URL above:
page = requests.get(URL)
#specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
soup = BeautifulSoup(page.text, "html.parser")
#printing soup in a more structured tree format that makes for easier reading
#print(soup.prettify())

############################extract job title######################################
def extract_job_title_from_result(soup): 
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
            jobs.append(a["title"])
    return(jobs)

#print(extract_job_title_from_result(soup))

########################extract company#########################################
def extract_company_from_result(soup): 
    companies = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in sec_try:
                companies.append(span.text.strip())
    return(companies)
 
#print(extract_company_from_result(soup))


#############################extract location############################################
def extract_location_from_result(soup): 
    locations = []
    spans = soup.findAll("span", attrs={"class": "location"})
    for span in spans:
        locations.append(span.text)
    return(locations)

#print(extract_location_from_result(soup))

#################################extract salary#########################################
def extract_salary_from_result(soup): 
    salaries = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        try:
            salaries.append(div.find('nobr').text)
        except:
            try:
                div_two = div.find(name="div", attrs={"class":"sjcl"})
                div_three = div_two.find("div")
                salaries.append(div_three.text.strip())
            except:
                salaries.append("Nothing_found")
    return(salaries)

#print(extract_salary_from_result(soup))

#################################extract job desc summary#########################################
def extract_summary_from_result(soup): 
    summaries = []
    spans = soup.findAll('span', attrs={'class': 'summary'})
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)

#print(extract_summary_from_result(soup))

max_results_per_city = 100
city_set = ['New+York','Chicago','San+Francisco','Austin','Seattle','Los+Angeles','Philadelphia','Atlanta','Dallas','Pittsburgh', 'Portland', 'Phoenix', 'Denver', 'Houston', 'Miami', 'Washington+DC', 'Boulder']
columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
sample_df = pd.DataFrame(columns = columns)


for city in city_set:
    for start in range(0, max_results_per_city, 10):
        page = requests.get('https://www.indeed.com/jobs?q=executive+director&l=' + str(city) + '&start=' + str(start))
        time.sleep(1)  #ensuring at least 1 second between page grabs
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
    for div in soup.find_all(name="div", attrs={"class":"row"}): 
    #specifying row num for index of job posting in dataframe
        num = (len(sample_df) + 1) 
    #creating an empty list to hold the data for each posting
        job_post = [] 
    #append city name
        job_post.append(city) 
    #grabbing job title
    for a in div.find_all(name="a", attrs={"data-tn-element":"jobTitle"}):
        job_post.append(a["title"]) 
    #grabbing company name
    company = div.find_all(name="span", attrs={"class":"company"}) 
    if len(company) > 0: 
      for b in company:
        job_post.append(b.text.strip()) 
    else: 
      sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
      for span in sec_try:
          job_post.append(span.text) 
    #grabbing location name
    c = div.findAll('span', attrs={'class': 'location'}) 
    for span in c: 
      job_post.append(span.text) 
    #grabbing summary text
    d = div.findAll('span', attrs={'class': 'summary'}) 
    for span in d:
        job_post.append(span.text.strip()) 
    #grabbing salary
    try:
      job_post.append(div.find('nobr').text) 
    except:
        try:
            div_two = div.find(name="div", attrs={"class":"sjcl"}) 
            div_three = div_two.find("div") 
            job_post.append(div_three.text.strip())
        except:
            job_post.append("Nothing_found") 
    #appending list of job post info to dataframe at index num
    sample_df.loc[num] = job_post

#saving sample_df as a local csv file — define your own local path to save contents 
sample_df.to_csv("ExecutiveDirector.csv", encoding='utf-8')
#pathName = "C:\Users\JiLi\Desktop\JobPosting.csv"
#sample_df.to_csv(pathName)
# 

