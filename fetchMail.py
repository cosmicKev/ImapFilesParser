import email
import email.utils

import imaplib
import os


class FetchEmail:

    connection = None
    error = None

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select(readonly=False) # so we can mark mails as read

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()

    @staticmethod
    def save_attachment(msg, download_folder="tmp"):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)

        return: file path to attachment
        """
        att_path = "No attachment found."
        for message in msg:
            for part in message.walk():
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition') is None:
                    continue

                filename = part.get_filename()
                att_path = os.path.join(download_folder, filename)

                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
        return att_path

    def delete_messages(self):
        (result, messages) = self.connection.search(None, '(Subject print)')
        for message in messages[0].split():
            self.connection.store(message,'+FLAGS','(\\Deleted)')
        self.connection.expunge()

    def fetch_3dprint_messages(self):
        """
              Retrieve unread messages
              """
        emails = []
        # typ, data = M.search(None, 'AFTER', '"01-Jan-2010"')
        (result, messages) = self.connection.search(None, '(Subject print)')
        if result == "OK":
            for message in messages[0].split():
                print(message)
                try:
                    ret, data = self.connection.fetch(message, '(RFC822)')
                except:
                    print("No new emails to read.")
                    self.close_connection()
                    exit()

                msg = email.message_from_bytes(data[0][1])
                if isinstance(message, str) == False:
                    emails.append(msg)
                response, data = self.connection.store(message, '+FLAGS', '\\Seen')

            return emails

        self.error = "Failed to retreive emails."
        return emails
