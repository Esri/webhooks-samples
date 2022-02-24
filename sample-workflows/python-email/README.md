# Creating a webhook receiver with python flask
This sample builds on the starter code from the [Developer/Python/Flask](../../Developer/python/flask/) example, adding a simple SMTP email server. You may need to work with your IT group to authorize the Python code with your SMTP server.

**Note**: This guide assumes that Python version 3 on Windows 10. You can follow this web site [Flask Web server](https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/2) for more info.

#### Step One: Install Python and modules
- Install [Python 3](https://www.python.org/downloads) 

- Install the required Python modules with pip

`pip install flask`

`pip install pyOpenSSL`

Begin by importing libraries:

```python
from flask import Flask, request
from OpenSSL import SSL
import os
import json
```

Set a path to write your received payloads to:
```python 
filename = 'C:\\temp\\webhookPayloads.txt' 
if os.path.exists(filename):
    append_write = 'a' # append if already exists
else:
    append_write = 'w' # make a new file if not
```

#### Step Two: Update the email server settings
Update the values for your SMTP server, email to and from, as well as the subject line in the [sendEmail.py](sendEmail.py)
```python
smtpServer = 'smtp.YOUR_EMAIL_SERVER.com'
fromEmail = "YOU@domain.com"
toEmail = "EmailGoesTo@domain.com"
subject = "A webhook was received"
```

#### Step Three: Set parameters for server:
Provide a certificate an key to secure the Python server, allowing it to be accessible over HTTPS.
```python

if __name__ == "__main__":   
    context = ('ssl.cert', 'ssl.key') # certificate and key file. Cannot be self signed certs    
    app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True) # will listen on port 5000    
```

#### Step Four: Run your web server
```bash
$ python webhookListener.py
 * Serving Flask app "webhookListener" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 235-907-892
 * Running on https://0.0.0.0:5000/ (Press CTRL+C to quit)
```
- Now you should be able to access the Webhook receiver by visiting `https://<machine.domain.com>:5000` URL
- You should see something similar to the screenshot below in your browser
<img src="../../images/WebhookListener-python.PNG" width="600"> 

#### Step Five: Configure your Webhook with the Receiver URL
Now you can use `https://<machine.domain.com>:5000` URL as your payload URL when creating your webhook. Test by configuring a webhook to make use of the receiver, perform the action and wait for an email.

