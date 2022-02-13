# -*- coding: utf-8 -*-
"""
Copy emails in docomo to gmail using imap4 protocol.
@author: kemunpus@docomo.ne.jp
"""

import email
import imaplib
import os
import ssl
from email.utils import parsedate_to_datetime

gmail_user = os.getenv("GMAIL_USER")
gmail_pass = os.getenv("GMAIL_PASS")
gmail_ssl = ssl.create_default_context()
gmail_host = "imap.gmail.com"
gmail_port = 993
gmail_inbox_folder = 'INBOX'

docomo_user = os.getenv('DOCOMO_USER')
docomo_pass = os.getenv('DOCOMO_PASS')
docomo_ssl = ssl.create_default_context()
docomo_ssl.set_ciphers('DEFAULT@SECLEVEL=1')
docomo_host = 'imap.spmode.ne.jp'
docomo_port = 993
docomo_inbox_folder = 'INBOX'
docomo_sent_folder = 'Sent'
docomo_saved_folder = 'Saved'

gmail_client = imaplib.IMAP4_SSL(host=gmail_host, port=gmail_port, ssl_context=gmail_ssl)
docomo_client = imaplib.IMAP4_SSL(host=docomo_host, port=docomo_port, ssl_context=docomo_ssl)

gmail_client.login(gmail_user, gmail_pass)
gmail_client.select(gmail_inbox_folder)

docomo_client.login(docomo_user, docomo_pass)
print(docomo_client.list())

docomo_client.select(docomo_inbox_folder)
response, docomo_mails = docomo_client.search(None, 'ALL')
for docomo_mail_id in docomo_mails[0].split():
    response, docomo_mail_data = docomo_client.fetch(docomo_mail_id, '(RFC822)')
    docomo_mail_body = docomo_mail_data[0][1]
    docomo_message = email.message_from_bytes(docomo_mail_body)
    docomo_mail_date = parsedate_to_datetime(docomo_message.get('Date'))
    response, result = gmail_client.append(gmail_inbox_folder, '', docomo_mail_date, docomo_mail_body)
    print(response, result)
    if response == 'OK':
        response, result = docomo_client.copy(docomo_mail_id, docomo_saved_folder)
        print(response, result)
        if response == 'OK':
            docomo_client.store(docomo_mail_id, '+FLAGS', '\\Deleted')

docomo_client.expunge()

docomo_client.select(docomo_sent_folder)
response, docomo_mails = docomo_client.search(None, 'ALL')
for docomo_mail_id in docomo_mails[0].split():
    response, docomo_mail_data = docomo_client.fetch(docomo_mail_id, '(RFC822)')
    docomo_mail_body = docomo_mail_data[0][1]
    docomo_message = email.message_from_bytes(docomo_mail_body)
    docomo_mail_date = parsedate_to_datetime(docomo_message.get('Date'))
    response, result = gmail_client.append(gmail_inbox_folder, '', docomo_mail_date, docomo_mail_body)
    print(response, result)
    if response == 'OK':
        response, result = docomo_client.copy(docomo_mail_id, docomo_saved_folder)
        print(response, result)
        if response == 'OK':
            docomo_client.store(docomo_mail_id, '+FLAGS', '\\Deleted')

docomo_client.expunge()

docomo_client.close()
gmail_client.close()
