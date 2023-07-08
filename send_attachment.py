import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from email.mime.text import MIMEText
from email.message import EmailMessage
import base64
import mimetypes

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
def aunthentication():
	creds = None
	if os.path.exists('token.json'):
		creds = Credentials.from_authorized_user_file('token.json', SCOPES)

	if not creds or not creds.valid:
		if creds and creds.expired and creds.refresh_token:
			creds.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file('client_secrets.json', SCOPES)
			creds = flow.run_local_server(port=0)

		with open('token.json', 'w') as token:
			token.write(creds.to_json())
	return creds
	
def prepare_and_send_email(recipient, subject, message_text, attachment):

	creds = aunthentication()
	try:

		service = build('gmail', 'v1', credentials=creds)
		msg = create_message('kshitij2020csai125@abesit.edu.in', recipient, subject, message_text, attachment)
		send_message(service, 'me', msg)

	except HttpError as error:

		print(f'An error occurred: {error}')
		
def create_message(sender, to, subject, message_text, attachment):
	message = EmailMessage()
	message['from'] = sender
	message['to'] = to
	message['subject'] = subject
	message.set_content(message_text)
	attachment_filename = attachment
	type_subtype, _ = mimetypes.guess_type(attachment_filename)
	maintype, subtype = type_subtype.split('/')
	with open(attachment_filename,'rb') as fp:
		attachment_data = fp.read()
	message.add_attachment(attachment_data, maintype, subtype, filename = attachment_filename)
	return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}
	
def send_message(service, user_id, message):
	try:
		message = (service.users().messages().send(userId=user_id,body=message).execute())
		print('Message Id: %s' % message['id'])
		return message
	except HttpError as error:
		print('An error occurred: %s' % error)
		
if __name__ == '__main__':
	prepare_and_send_email('kshitij.antiphishing@gmail.com', 'Greetings from Kshitij', 'This is a test email for our upcoming app.', 'pig.png')
















