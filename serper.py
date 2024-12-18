import http.client
import json
from dotenv import load_dotenv
import os

load_dotenv()

def serperquery(query):
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
    "q": query
    })
    headers = {
    'X-API-KEY': os.getenv("Serper_api"),
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return(data.decode("utf-8"))


#Serper tool for image generation


conn = http.client.HTTPSConnection("google.serper.dev")
payload = json.dumps({
  "q": "apple inc",
  "gl": "in"
})
headers = {
  'X-API-KEY': 'e40490d0083cd56dd95e52f41841364bbe64e6aa',
  'Content-Type': 'application/json'
}
conn.request("POST", "/images", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))


#Serper tool for fetching Locations

import http.client
import json

conn = http.client.HTTPSConnection("google.serper.dev")
payload = json.dumps({
  "q": "apple inc"
})
headers = {
  'X-API-KEY': 'e40490d0083cd56dd95e52f41841364bbe64e6aa',
  'Content-Type': 'application/json'
}
conn.request("POST", "/places", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))