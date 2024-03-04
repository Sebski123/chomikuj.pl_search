import json
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

SEARCH_STRING = "whatever you want to search for"

# Get the session ID, verification token, GUID, and RCID from the browser's cookies
SESSION_ID = ''
VERIFICATION_TOKEN = ''
GUID = ''
RCID = 's'

COOKES = {
    'ChomikSession': SESSION_ID,
    '__RequestVerificationToken_Lw__': VERIFICATION_TOKEN,
    'guid': GUID,
    'rcid': RCID
}

# Define a mapping of Polish month abbreviations to English month abbreviations
MONTH_MAPPING = {
    'sty': 'Jan',
    'lut': 'Feb',
    'mar': 'Mar',
    'kwi': 'Apr',
    'maj': 'May',
    'cze': 'Jun',
    'lip': 'Jul',
    'sie': 'Aug',
    'wrz': 'Sep',
    'paź': 'Oct',
    'lis': 'Nov',
    'gru': 'Dec'
}

# Define the format of the input date string with the English month abbreviation
DATE_FORMAT = "%d %b %y %H:%M"

URL = "https://chomikuj.pl/action/SearchFiles/Results"


HEADERS = {
    # Convert cookoes to a string
    'Cookie': '; '.join([f'{k}={v}' for k, v in COOKES.items()]),
}


def retrive_single_page(payload):
    response = requests.request("POST", URL, headers=HEADERS, data=payload)

    # # save the response to a file
    # with open(f'response_{payload["Page"]}.html', 'w', encoding="utf-8") as file:
    #     file.write(response.text)
    # exit()

    # Parse the response
    soup = BeautifulSoup(response.text, 'html.parser')

    results = []

    for file in soup.find_all(class_=re.compile("filerow.*fileItemContainer")):
        # print(file)
        if (file.find(class_=re.compile("filename.*")) == None):
            continue
        result = {}
        result["name"] = file.find(class_=re.compile("filename.*")).find('a')["title"]
        result["url"] = "https://chomikuj.pl" + file.find(class_=re.compile("filename.*")).find('a')["href"]
        date_string = file.find(class_=re.compile("date.*")).text
    # Convert the Polish month abbreviation to English
        for polish_month, english_month in MONTH_MAPPING.items():
            date_string = date_string.replace(polish_month, english_month)

    # Parse the input date string to a datetime object
        date_object = datetime.strptime(date_string, DATE_FORMAT)
        result["date"] = date_object.isoformat()

        results.append(result)
    return results


results = []

for page in range(51):
    # create a payload with the keys: FileName and Page
    payload = {
        'FileName': '{SEARCH_STRING}',
        'Page': page
    }

    print(f"Retrieving page {page}...")

    results += retrive_single_page(payload)

# Print the results
# for result in results:
#     print(result["name"])
# print(results)

# save the results to a file
with open('results.json', 'w') as file:
    json.dump(results, file, indent=4)

# Save the response to a file
# with open('response.html', 'w', encoding="utf-8") as file:
#     file.write(response.text)
