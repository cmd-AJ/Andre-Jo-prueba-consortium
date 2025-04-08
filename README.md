# Andre-Jo-prueba-consortium


### CHECK OUT THE WEBPAGE 📽
    http://3.147.6.53/


# NOTAS
- NO utilizar la version de Python Reciente 3.13


## Used Postgresql as main database, also loaded the data with the following command
    python manage.py loaddata liquidations/fixtures/db/liquidations.json
    python manage.py loaddata spending_control/fixtures/db/spendings.json

### To check if the data is loaded use this endpoint
    #Get data from postgresql spendings
    http://127.0.0.1:8000/api/spendings/ ##Loaded from data of spendings.json
    

    #Get data from postgresql liquidations
    http://127.0.0.1:8000/api/liquidity/ ##Loaded from data of liquidations.json NO hay etapa establecida es de antes de los incisos



# Instalación

## Backend
    python -m venv venv
    source venv/bin/activate
    python3.11 pip install -r requirements.txt


## Frontend
    npm install vite@latest
        Select Vue.js depends if you like typescript or javascript 


# Etapa 1

Herramientas a utilizar 

DOCKER (DOCKER COMPOSE)
Para Correr el contenedor se debe utilizar el comando

    sudo docker compose up --build -d #Las flag build es para construir el contenedor y -d es para correrlo en el background o sea no hay necesidad de interactuar

Dentro del Docker compose contiene una base de datos PostgreSQL donde expone el puerto 5432


# DJANGO (Backend)

## Sub Instalaciones
Para crear un proyecto se utiliza el comando
    django-admin startproject <name>


Para crear una app se utiliza el comando
    django-admin startapp <name>


Principalmente utilizado para los servicios de Rest API

La aplicación (carpeta) notifrecepction es utilizado para llamar a los endpoints para obtener los datos de Postgresql y traer esos datos hacia el Frontend


## Endpoints
        send_notif    #Envia los datos tipo JSON hacia la base de datos de PostgreSQL
        sendmail      #Utilizando la API NOTIFICATIONS API se envia los datos de las notificaciones hacia el correo.
        #Tomar Nota, Se utilizo .env para no revelar la api key y otros secretos
        spendings     # Utilizando loaddata se cargo los datos y para comprobar se utiliza este endpoint para conseguir los datos de la base de datos
        liquidity     # Utlizado con Loaddata, consigue los datos de liquidity
        users         # Consigue los usuarios disponibles para el colaborador de la firma
        getnotification #Consigue las notificaciones que fueron enviadas.


# VUE.JS

Correr Vue.JS localmente

Componentes Importantes
    Formulario: Tiene todos los componentes requeridos a enviar para la base de datos y el correo. 
        Utilización del Fetch para conseguir los endpoints que requiere para enseñar las notificaciones y usuarios disponibles




RECURSOS EXTRAS
https://app.notificationapi.com/
