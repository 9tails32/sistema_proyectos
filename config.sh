
#!/bin/bash

# Este script esta pensado para la instalacion del proyecto de desarrollo en un$
# Se debe correr con permisos de super usuario para no tener ningun problema a $

pip install virtualenv
virtualenv env
. env/bin/activate
echo "Hola"
pip install -r requirements.txt
./manage.py runserver


