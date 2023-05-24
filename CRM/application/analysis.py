import requests
url = "https://www.fast2sms.com/dev/bulkV2"
querystring = {
    "authorization": "2Dq3l5SmUP7rOwvaeKWc1VFykRguBYf0N4AC8nLpXbdZGo6sjxOWlkiJxNPSzqaQoyTIHwb7GfMAEUZ3",
    "message": "This is test Message sent from  Python Script using REST API.",
    "language": "english",
    "route": "q",
    "numbers": "9346184642, 9704292046"}
headers = { 'cache-control': "no-cache"}
try:
    response = requests.request("GET", url,headers = headers, params = querystring)
    print("SMS Successfully Sent")
except:
    print("Oops! Something wrong")