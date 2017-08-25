import urllib2
import urllib
import sys
import base64
import json
import uuid
from  __builtin__ import any as b_any

base_url = 'https://westus.api.cognitive.microsoft.com/'
account_key = '5d4258fdaf7d4ddabc5cafb398b86142'
headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': account_key}
num_detect_langs = 1

technology_skills=["ai", "blockchain", "bots", "cloud platforms", "cognitive computing", "computer vision", "conversational ui","deep learning",
        "devops", "edge intelligence","edge sensing", "event stream processing", "iot platforms","machine learning","nlp","predictive analytics",
        "real time computing","robotic process automation","serverless architecture"]

healthcare_key_words = ["ACA","ACO","Care Profile","Clinical Trial","EHR","EMR","Event Based Medicine","HIPAA","HL7","Hospital","Insurance",
                        "Medicaid", "Medicare", "Member","MLR","Outcomes","Patient","Payer","Pharma","Provider", "Quality of Care", "snowmeds",
                        "STARS","Telemedicine","Wellness"]

healthcare_key_words = [element.lower() for element in healthcare_key_words]

def extract_keywords(input_texts):
    batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
    req = urllib2.Request(batch_keyphrase_url, input_texts, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = eval(result)
    for item in obj['documents']:
        key = item.get("keyPhrases")
        return key

def convert_text_to_API_Format(text):
    text = text.encode("utf-8")
    jsonString = '{"documents":[{"id":"' + str(uuid.uuid4()) +'","text":"' + str(text) +'"}]}'
    return jsonString

def compare_key_words(words):
    health_flag = False
    tech_flat = False
    if words is None or len(words) == 0:
        return False
    for item in technology_skills:
        if(compare_technology(item, words)):
            #return True
            tech_flat = True
            break
        else:
            continue

    for word in healthcare_key_words:
        if compare_healthcare(word, words):
            #return True
            health_flag = True
            break
        else:
            continue
    if tech_flat and health_flag:
        return True
    else:
        return False


def compare_technology(technology_skill,words):
    words = [item.lower() for item in words]
    return b_any(technology_skill in x for x in words)

def compare_healthcare(healthcare_words,words):
    words = [item.lower() for item in words]
    return b_any(healthcare_words in x for x in words)

print (compare_key_words(['machine Learning', 'mathematical methodologies']))
# key_word = extract_keywords(input_texts)
# print(key_word)