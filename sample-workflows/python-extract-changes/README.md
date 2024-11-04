# Extracting Changes from Feature Service
The webhook payoad includes a changesUrl property (see example at the bottom). This callback URL to the extract changes resource of the feature service provides the ability to retrieve the edit history from the feature service. The code here demonstrates how to make the calls to retrieve the features. Similar to the **Python Flask** workflow, the `webhookListner.py` handles incoming webhook messages and calls extract changes for each request. 

Note: The `ec.py` file includes a `"__main__"` call which allows the extract changes code to be called directly for testing. You will need to supply the full extract changes URL with server generation numbers.


#### Step One: Install Python and modules
- Install [Python 3](https://www.python.org/downloads) 

- Install the required Python modules with pip

`pip install requests`

`pip install flask`

`pip install pyOpenSSL`


#### Step Two: Update the code:

- Update the variables for your ArcGIS Enterprise deployment inside the `webhookListener.py` file.

-**Note**: The script hardcodes credentials and generates a token to retrieve features from a secured feature service. Other authentication mechanisms (should they be needed) are available using the [ArcGIS Python API](https://developers.arcgis.com/python/latest/). 

- Take note of the `getExtractChanges` method. This method will return new, updated, and deleted features for the extract changes API call. If necessary, update the default parameters to return only features your workflow requires. Consult the [Extract Changes](https://developers.arcgis.com/rest/services-reference/enterprise/extract-changes-feature-service/) help topic for information about parameters and acceptable values.


#### Step Two: Set parameters for server:
Provide a certificate an key to secure the Python server, allowing it to be accessible over HTTPS.
```python

if __name__ == "__main__":   
    context = ('ssl.cert', 'ssl.key') # certificate and key file. Cannot be self signed certs    
    app.run(host='0.0.0.0', port=5000, ssl_context=context, threaded=True, debug=True) # will listen on port 5000    
```

#### Step Three: Run your web server
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

#### Step Four: Configure your Webhook with the Receiver URL
Now you can use `https://<machine.domain.com>:5000` URL as your payload URL when creating your webhook. Test by configuring a webhook to make use of the receiver, perform the action and wait for an email.


#### Example wehbook payload

```
{
  "serviceType": "FeatureServer",
  "changesUrl": "https://server.com/server/rest/services/ServiceName/FeatureServer/extractChanges?serverGens=%5B1730385704442,1730385704443%5D",
  "name": "Webhook Name",
  "id": "c4a7db24-0c5e-4a00-9103-0c7d2fdc03b4",
  "folderName": "",
  "serviceName": "ServiceName",
  "events": [
    {
      "eventType": "FeaturesCreated",
      "when": 1730385704000
    }
  ]
}
```