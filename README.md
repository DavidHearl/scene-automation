## Create Virtual Environment

- Create the virtual environment
``` 
py -m venv ./venv
```
- Load the script
```
source ./venv/scripts/activate
```

- Check the pip location has changed
```
which pip
```

- To exit the Virtual Envrionment
```
deactivate
```

## Project Deployment

- Install Dependancies
```
python.exe -m pip install --upgrade pip
pip install -r requirements.txt

pip3 install 'django<4' gunicorn
pip3 install dj_database_url==0.5.0 psycopg2
pip3 install dj3-cloudinary-storage
pip3 install urllib3==1.26.15
```

```
pip freeze --local > requirements.txt
```

- Create project
```
django-admin startproject scene_automation .
python manage.py startapp front_end

python manage.py migrate
python manage.py runserver
```