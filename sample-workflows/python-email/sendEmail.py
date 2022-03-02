"""  Copyright 2021 Esri
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License. """

import smtplib
from email.mime.text import MIMEText

""" Update the following variables for your SMTP server and To / From email addresses.
This is a very simple email example and may not work within your environment. Work with
your IT group to leverage your internal email capabilities.
SMTPLIB - https://docs.python.org/3/library/smtplib.html
"""
smtpServer = 'smtp.YOUR_EMAIL_SERVER.com'
fromEmail = "YOU@domain.com"
toEmail = "EmailGoesTo@domain.com"
subject = "A webhook was received"


def send(msg, f=fromEmail, t=toEmail, s=subject):
    """ The msg is not parsed. You can parse the JSON message in the server listener, or do it here.
        This code simply sends the JSON message directly through.    
    """

    msg = MIMEText(msg)
    msg['Subject'] = s
    msg['From'] = f
    msg['To'] = t

    s = smtplib.SMTP(smtpServer)
    s.sendmail(f, [t], msg.as_string())
    s.quit()
