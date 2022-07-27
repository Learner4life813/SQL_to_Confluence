import requests
import os
import pyodbc
import base64
import datetime
import sys

#DB parameters
server = ''
database = 'Thesaurus2'
query = '''SELECT cq.Name,MAX(SourceDate) AS LatestLoadDate FROM lp
            INNER JOIN cq ON cq.CodeQualifierID = lp.CodeQualifierID
            GROUP BY cq.Name
            ORDER BY cq.Name
            FOR JSON PATH'''

#confluence page parameters
page_id = ''
att_id = ''
url = 'https://<confluence>/rest/api/content/'+page_id+'/child/attachment/'+att_id+'/data'
file_name = 'Attachment.txt'
file_path = os.path.join(os.getcwd(),file_name)

#confluence authorization
bearer_token_end_date = datetime.datetime(2022,7,31)
if (datetime.datetime.now() >= bearer_token_end_date):
    sys.exit('The beaer token is not valid. Create a new one.')

#every time the bearer token is replaced, generate the encoded string and assign to bearer_token_encoded
#remove the bearer token literal string from the code
#bearer_token = ''
#print(base64.b64encode(bearer_token.encode("utf-8")))
bearer_token_encoded = b'Tnprd09EUXpNak15TWpNek9xM1hmb1NnTXlRS0VKTjdNRGt2bnVZSDlBQkk='
headers = {
   "Authorization": "Bearer " + base64.b64decode(bearer_token_encoded).decode("utf-8"),
   "X-Atlassian-Token": "nocheck"
}

try:
    cnxn = pyodbc.connect('Driver=SQL Server;SERVER='+server+';DATABASE='+database+';Trusted_Connection=Yes')
    cursor = cnxn.cursor()
    cursor.execute(query) 

    #assuming the query returns only one field, write to the file
    with open(file_path, 'w') as file:
        file.write(cursor.fetchone()[0])

    payload = {"file": open(file_path, 'rb'), "minorEdit": "true"}
    #update the content of the attachment
    response = requests.post(url, headers = headers, files = payload)
    if response.status_code == 200:
        print("Update successful!")

except Exception as e:
    print(e)
