# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 10:57:04 2017

@author: JiLi
"""

# -*- coding: utf-8 -*-
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
columns = ["city", "job_title","company_industry","company_name", "location", "summary", "salary"]
#columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
sample_df = pd.DataFrame(columns=columns)

for city in city_set:
    for start in range(0, max_results_per_city, 10):
        page = requests.get('https://www.indeed.com/jobs?q=executive+director&l=' + str(city) + '&start=' + str(start))
        time.sleep(1)  # ensuring at least 1 second between page grabs
        soup = BeautifulSoup(page.text, "lxml", from_encoding="utf-8")
    for div in soup.find_all(name="div", attrs={"class": "row"}):
        # specifying row num for index of job posting in dataframe
        num = (len(sample_df) + 1)
        # creating an empty list to hold the data for each posting
        job_post = []
        # append city name
        job_post.append(city)
        # grabbing job title
    for a in div.find_all(name="a", attrs={"data-tn-element": "jobTitle"}):
        job_post.append(a["title"])
        url = "https://www.indeed.com" + a["href"]
        # print url;
        if url != None:  # if company link exists, access it. Otherwise, skip.
            try:
                page = requests.get(url)
                # specifying a desired format of “page” using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
                soup = BeautifulSoup(page.text, "html.parser")
                # grabbing company and industry info: get into a deep layer
                temp = soup.find_all(name="span", attrs={"class":"summary"})
                if temp.__len__() == 0:
                    job_post.append("No Summary found")
                else:
                    for b in soup.find_all(name="span", attrs={"class": "summary"}):
                        # job_post.append(b.text.strip()) # append the first <p> which is the companry info and industry info
                        try:
                            job_post.append(b.find('p').text.strip())
                            print(b.find('p').text.strip())
                            print("------------------------------------------------------------")
                        except:
                            print("haha")
                            job_post.append("Nothing_found")
                            # job_post.append("Nothing_found")
                            # print(sample_df[['company_industry']])
                            # print(sample_df[sample_df.columns[0:3]])
            except:
                print("invalid url")
                job_post.append("invalid url")

        else:
            job_post.append("Nothing_found")
            print("url not found")

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
    for span in d:
        job_post.append(span.text.strip())
        # grabbing salary
    try:
        job_post.append(div.find('nobr').text)
    except:
        try:
            div_two = div.find(name="div", attrs={"class": "sjcl"})
            div_three = div_two.find("div")
            job_post.append(div_three.text.strip())
        except:
            job_post.append("Nothing_found")
            # appending list of job post info to dataframe at index num
    sample_df.loc[num] = job_post

# saving sample_df as a local csv file — define your own local path to save contents
sample_df.to_csv("JobsWithCompanyBackground.csv", encoding='utf-8')
# pathName = "C:\Users\JiLi\Desktop\JobPosting.csv"
# sample_df.to_csv(pathName)
#

