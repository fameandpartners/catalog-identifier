Fame and Partners Facebook Catalog Matching App
==============================


What Is This?
-------------

This is a simple application developed for Fame and Partners with the purpose of matching custom product GUI to existing
GUIs recorded in the Facebook product catalog. This app exposes an API endpoint and is currently called via 
Google Tag Manager.

How To Use This
---------------

1. Install all of the dependencies in requirements.txt via `pip install -r requirements.txt`
2. Run the app either via `python runapp.py` (for testing), or `gunicorn --bind 0.0.0.0:$PORT application` 
(wsgi implementation)

Deployment
---------------
This app is currently deployed using heroku, in most cases you need the following two commands.

1. `heroku login`
2. `git push heroku master`

If you wish to change how this app is ran on heroku, please change the Procfile

For more detailed instruction please follow the following link:

https://medium.com/the-andela-way/deploying-a-python-flask-app-to-heroku-41250bda27d0


Making Requests
---------------

This app uses flask-restplus, a library that introduces input marshalling and swagger documentation to the app. 
To view the app documentation, simply visit the root directory of your local or the heroku deployment. 

Support
---------------

This simple app is developed by Humanlytics LLC, for any support questions, please contact bill@humanlytics.co. Thanks!