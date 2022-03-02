# Project Name: Vest Challenge

## Description
---
API that simulate a virtual trading environment written with Python using FastAPI, SQL Alchemy.

### Construction 🛠️
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

#### Note 🔍
The FastAPI application will probably throw an exception the first time, because it will try to connect to the PostgreSQL service that is still initializing for the first time; in this case wait for PostgreSQL to fully initialize first and then run the command `docker-compose restart vest_challenge` in another terminal to restart the crashed service.

## Project Structure
---
The following diagram describe the project structure used for this API
```
challenge_vest
│   .gitignore          
│   Dockerfile
│   README.md                   
│   docker-compose.yml     
│   requirements.txt          
│
└───app
│   │   .env
│   │   exception.py
│   │   main.py
│   │   util.py
│   │
│   └───api                     Contains all modules for API uses
│   │   │
│   │   └───stocks              Module Stock: Contains all related stocks endpoints
│   │   │   │   routes.py       Routes for stocks
│   │   │   │
│   │   │   └───dtos            Uses for Data Transfer Objects needed
│   │   │   │
│   │   │   └───repositories    Contains logic with the databases and bussiness rules
│   │   │   │
│   │   │   └───schemas         Keep schemas used for this module
│   │   
│   └───core                    Used to manage settings of the application
│   │   
│   └───services                Modules for external services which the application interact
│   │   │
│   │   └───db                  Module for interact with the database
│   │   │
│   │   └───nasdaq              Module for NASDAQ Communication
│   │   
│   └───tests                   Contains all unit tests for application
│   │   
│   └───postman                 Contains documented examples of endpoints usage

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


## Testing ⚙️

To run the tests:

- Have the services running using `docker-compose up`.
- In another console, run `docker exec -it vest_challenge pytest`.


### Authors ✒️

* **Author:** Javier Quintana, <javier.taipe.1998@gmail.com>

