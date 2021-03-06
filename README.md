# Project Name: Vest Challenge

## Description
---
API that simulate a virtual trading environment written with Python using FastAPI, SQL Alchemy.

### Construction π οΈ
* **Language:** Python 3
* **Framework:** FastAPI, SQL Alchemy
* **Database:** PostgreSQL

## Requirements
---
- Docker installed

## Installation and execution
---
Clone or Fork the project.

Run ```docker-compose``` command inside **docker-python** folder.

* Building the containers: ```docker-compose build```

* Starting the services: ```docker-compose up -d```

* Stoping the services: ```docker-compose stop```

By default the microservice will run under the following port:
- vest-challenge: 8000

#### Note π
The FastAPI application will probably throw an exception the first time, because it will try to connect to the PostgreSQL service that is still initializing for the first time; in this case wait for PostgreSQL to fully initialize first and then run the command `docker-compose restart vest_challenge` in another terminal to restart the crashed service.

## Project Structure
---
The following diagram describe the project structure used for this API
```
challenge_vest
β   .gitignore          
β   Dockerfile
β   README.md                   
β   docker-compose.yml     
β   requirements.txt          
β
ββββapp
β   β   .env
β   β   exception.py
β   β   main.py
β   β   util.py
β   β
β   ββββapi                     Contains all modules for API uses
β   β   β
β   β   ββββstocks              Module Stock: Contains all related stocks endpoints
β   β   β   β   routes.py       Routes for stocks
β   β   β   β
β   β   β   ββββdtos            Uses for Data Transfer Objects needed
β   β   β   β
β   β   β   ββββrepositories    Contains logic with the databases and bussiness rules
β   β   β   β
β   β   β   ββββschemas         Keep schemas used for this module
β   β   
β   ββββcore                    Used to manage settings of the application
β   β   
β   ββββservices                Modules for external services which the application interact
β   β   β
β   β   ββββdb                  Module for interact with the database
β   β   β
β   β   ββββnasdaq              Module for NASDAQ Communication
β   β   
β   ββββtests                   Contains all unit tests for application
β   β   
β   ββββpostman                 Contains documented examples of endpoints usage

```

## Endpoints
---
The following endpoints have been developed for this API:

> -  **GET /stocks/my** <br/>
> Get detailed information about your shares
> -  **GET /stocks/history/{symbol}** <br/>
> Get the price records of a stock
> -  **POST /stocks/transfers** <br/>
> Allows to create a transaction

Example:

```curl 
curl --request POST \
--url http://localhost:8000/stocks/transfers \
--header 'Content-Type: application/json' \
--data '{
    "qty": 5,
    "symbol": "aapl",
    "transaction_type": "buy"
}'
```


## Testing βοΈ

To run the tests:

- Have the services running using `docker-compose up`.
- In another console, run `docker exec -it vest_challenge pytest`.


### Authors βοΈ

* **Author:** Javier Quintana, <javier.taipe.1998@gmail.com>

