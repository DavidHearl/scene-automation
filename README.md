## Areas for possible Improvement
[] - Priority List
[] - Area in S**2m
[] - Number of points in the cloud
[] - Estimated number of scans
[] - Area Type

## Create Virtual Environment

``` 
# Create the virtual environment
py -m venv ./venvwin

# Load the script
source ./venvwin/scripts/activate

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