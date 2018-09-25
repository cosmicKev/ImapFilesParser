import getpass
from fetchMail import FetchEmail

mail_server = 'imap.gmail.com'
print('GMAIL email attatchment parser using string: print in subject.')
print('Made by: Kevin Filipe')

username = input('Enter your email: ')
password = getpass.getpass('Enter your password: ')
fm = FetchEmail(mail_server,username,password)

# Searching for messages that has the word print as email subject
msg = fm.fetch_3dprint_messages()
# Save files in each email in tmp folder
fm.save_attachment(msg, 'tmp')
# Move messages to trash at email.
fm.delete_messages()
