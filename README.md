# Andre-Jo-prueba-consortium

# NOTAS
### NO utilizar la version de Python Reciente 3.13


## Used Postgresql as main database, we also loaded the data with the following command
    python manage.py loaddata liquidations/fixtures/db/liquidations.json
    python manage.py loaddata spending_control/fixtures/db/spendings.json

### To check if the data is loaded use this endpoint
    #Get data from postgresql spendings
    http://127.0.0.1:8000/api/spendings/ ##Loaded from data of spendings.json
    

    #Get data from postgresql liquidations
    http://127.0.0.1:8000/api/liquidity/ ##Loaded from data of liquidations.json