#######################################################################################
# This is a sample to get the message list from Gmail
#######################################################################################
import httplib2
import imaplib,email,email.Header
import base64

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import SignedJwtAssertionCredentials
import pprint

def lambda_handler(event, context):
    try:
       main()
    except Exception:
       traceback.print_exc()
       sys.stderr.flush()
       sys.exit(1)

def main():
    pp = pprint.PrettyPrinter(indent=4)
    
    SERVICE_ACCOUNT_ID="your service account id"
    KEY_SECRET="your secret key"
    GMAIL_ACCOUNT="your gmail account"
    
    f = open("privatekey.pem","rb")
    key = f.read()
    f.close()
    
    credentials = SignedJwtAssertionCredentials(
        SERVICE_ACCOUNT_ID,
        key,
        scope="https://www.googleapis.com/auth/gmail.readonly",
        sub=GMAIL_ACCOUNT)
    http = httplib2.Http()
    
    http = credentials.authorize(http)
    service = build("gmail", "v1", http=http)
    
    message_list = service.users().messages().list(userId='me',
                                                    #labelIds=label_ids,
                                                    #pageToken=page_token,
                                                    maxResults=10,
                                                    q='is:unread'
                                                    ).execute()
    for message in message_list['messages']:
       message_detail = service.users().messages().get(userId='me', id=message['id'],format='metadata').execute()

       for element in message_detail['payload']['headers']:
          if element['name'] == 'Subject':
             print element['value']

if __name__ == '__main__':
        main()

