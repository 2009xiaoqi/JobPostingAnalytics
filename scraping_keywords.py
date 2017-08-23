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
#input_texts = '{"documents":[{"id":"1","text":"hello world, let us see the eclipse outside"}]}'
num_detect_langs = 1
#test = "Position Summary The Executive Director is the chief executive officer of WNS and is responsible on"
technology_skills=["ai", "blockchain", "bots", "cloud platforms", "cognitive computing", "computer vision", "conversational ui","deep learning",
        "devops", "edge intelligence","edge sensing", "event stream processing", "iot platforms","machine learning","nlp","predictive analytics",
        "real time computing","robotic process automation","serverless architecture"]

def extract_keywords(input_texts):
    batch_keyphrase_url = base_url + 'text/analytics/v2.0/keyPhrases'
    req = urllib2.Request(batch_keyphrase_url, input_texts, headers)
    response = urllib2.urlopen(req)
    result = response.read()
    obj = eval(result)
    for item in obj['documents']:
        key = item.get("keyPhrases")
        return key


#input_texts = '{"documents":[{"id":"1","text":"hello world, let us see the eclipse outside"}]}'
def convert_text_to_API_Format(text):
    text = text.encode("utf-8")
    jsonString = '{"documents":[{"id":"' + str(uuid.uuid4()) +'","text":"' + str(text) +'"}]}'
    return jsonString


def compare_key_words(words):
    if words is None or len(words) == 0:
        return False
    for item in technology_skills:
        if(compare_string(item, words)):
            return True
        else:
            continue
    return False


def compare_string(technology_skill,words):
    words = [item.lower() for item in words]
    return b_any(technology_skill in x for x in words)

print (compare_key_words(['machine Learn', 'mathematical methodologies']))
    # key_word = extract_keywords(input_texts)
# print(key_word)