"""Unpaid public availability examples. Never signs, pays or follows a payment challenge."""
import json,pathlib,urllib.request,urllib.error
ROOT=pathlib.Path(__file__).resolve().parent
for offer in json.loads((ROOT/'verified-offerings.json').read_text()):
    body=(ROOT/(offer['slug']+'-request.json')).read_bytes()
    req=urllib.request.Request(offer['endpoint'],data=body,method='POST',headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=30) as response:
            print(offer['slug'],response.status,'unexpected successful response; no payment attempted')
    except urllib.error.HTTPError as error:
        print(offer['slug'],error.code,'payment challenge present:',bool(error.headers.get('payment-required')))
    except urllib.error.URLError as error:
        print(offer['slug'],'network unavailable:',error.reason)
