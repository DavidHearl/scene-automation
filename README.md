# TODO:
- Embed the Scan Viewer for each venue, or a link etc.
- Embed the live location of the ship
- Pull the ship itinerary

## Areas for possible Improvement
[] - Area in S**2m
[] - Area Type

## Create Virtual Environment

``` 
# Create the virtual environment
py -m venv virtual_environment

# Load the script
source ./virtual_environment/scripts/activate

# Check pip location has changed
which pip

# Exit virtual environment
deactivate
```

## Install Dependancies

```
pip install -r requirements.txt
python.exe -m pip install --upgrade pip

pip3 install 'django<4' gunicorn
pip3 install dj_database_url==0.5.0 psycopg2
pip3 install dj3-cloudinary-storage
pip3 install urllib3==1.26.15
pip install django-allauth
```

```
pip freeze --local > requirements.txt
```

## Heroku CLI Login
```
# Login
heroku login 

# Search for the list of apps
heroku apps

# 
heroku config:get DATABASE_URL -a scene-automation

psql DATABASE_URL

```



## Django Allauth
Copy the templates from the correct directory
```
ls C:\Users\DavidH-LA\AppData\Local\Programs\Python\Python310\pip-modules\lib\

cp -r C:/Users/DavidH-LA/AppData/Local/Programs/Python/Python310/lib/site-packages/allauth/templates/* ./templates
```

## Project Deployment
```
django-admin startproject scene_automation .
python manage.py startapp front_end

python manage.py migrate
python manage.py runserver
```