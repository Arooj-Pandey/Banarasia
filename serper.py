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