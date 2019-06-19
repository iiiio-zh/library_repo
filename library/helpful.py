# launch sql in terminal
sudo mysql -uroot -p
# launch sql workbench
mysql-workbench

!! django
# cd into directory where you want project
django-admin startproject PROJECT_NAME
# run django server
 python3 manage.py runserver

# DATABASE in settings.py should look like this
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourdbpassword',
    }
}

# check your app
http://127.0.0.1:8000/
localhost:8000/[directory_name]

# if port in use
netstat -ntlp
kill process

# remember to use pip3 to install your stuff!

# django to database
# after you have defined models, you need to activate them
python3 manage.py makemigrations APP_NAME
python3 manage.py sqlmigrate APP_NAME NUMBER
python3 manage.py migrate

# delete other users
deluser USERNAME

# at base project urls, add pointers to your app
# say you made an app called yourapp
# you must have django point to yourapp
# baseproject/baseproject/urls.py
urlpatterns = [
    path('yourapp/', include('yourapp.urls')),
    path('admin/', admin.site.urls),
]
