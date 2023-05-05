# FastAPI-course

### Navigation:

##### 1. [Installation and start](#first_lesson)
##### 1.1.  [Documentation and site adress ](#doc)
##### 2. [Endpoints](#second_lesson)
##### 3. [Data Validation](#third_lesson)
##### 4. [Data base and migrations](#fourth_lesson)

## Lessons:


### 1. Installation and start<a name = "first_lesson"></a>:

Cd ***project_root*** 
for e.g.:
> cd /home/bogdan/PycharmProjects/FastAPI-course

Create "filename".py (for e.g.: main.py)

Write in terminal these commands:

> python -m venv venv

> source venv/bin/activate

> pip install fastapi[all]

Write this code in file:

```python
from fastapi import FastAPI

app = FastAPI()     # entry point to our web-app


@app.get("/")   # GET-request
def hello():
    return "Hello world!"
```

To start write this in terminal:

> uvicorn main:app --reload

<a name = "doc"></a>
Site will run on localhost: http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs#/default

Redoc: http://127.0.0.1:8000/redoc

---

### 2. Endpoints<a name = "second_lesson"></a>:

Write DB immitation:
```python
# DB example:
fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"}
]
```
Rewrite our entry-point variable:
```python
app = FastAPI(
    title="Trading App" # title
)
```
Then rewrite our get-method to fetch user from DB by id(Primary Key).

```python
@app.get("/users/{user_id}")    # GET-request
def get_user(user_id):
    return [user for user in fake_users if user["id"] == user_id]
```
Create fake trades to write another GET-method vie path-parameters:
```python
fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12}
]
```
Write GET-method with query-parameters to return trades with pagination
```python
@app.get("/trades")
def get_trades(limit: int = 10, offset: int = 10):
    return fake_trades[offset:][:limit]
```
* limit - trades limit
* pagination - number of trades on one page

Write combined POST-method to change username:
```python
fake_users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"}
]


@app.post("/user/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}
```
All code:
```python
from fastapi import FastAPI

# entry point to our web-app
app = FastAPI(
    title="Trading App"  # title
)

# DB example:
fake_users = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"}
]

# http://127.0.0.1:8000/users/1
@app.get("/users/{user_id}")  # GET-request
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]


fake_trades = [
    {"id": 1, "user_id": 1, "currency": "BTC", "side": "buy", "price": 123, "amount": 2.12},
    {"id": 2, "user_id": 1, "currency": "BTC", "side": "sell", "price": 125, "amount": 2.12}
]


# http://127.0.0.1:8000/trades/?limits=1&offset=0
@app.get("/trades")
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


fake_users2 = [
    {"id": 1, "role": "admin", "name": "Bob"},
    {"id": 2, "role": "investor", "name": "John"},
    {"id": 3, "role": "trader", "name": "Matt"}
]

# http://127.0.0.1:8000/user/1
@app.post("/user/{user_id}")
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get("id") == user_id, fake_users2))[0]
    current_user["name"] = new_name
    return {"status": 200, "data": current_user}
```

---

### 3. Data validation<a name="third_lesson"></a>

We need data validation to correct work of our server, if wrong data was sent that will cause errors.

Also data validation provides good documentation issues

![image](https://user-images.githubusercontent.com/65871712/235636652-1a53b1a7-9eeb-4675-86c6-c46b13ed8fe8.png)

To resolve problem with wrong data and add good documentation we should use Pydantic library:
```python
from pydantic.main import BaseModel 

class Trade(BaseModel):
    id: int
    user_id: int
    currency: str
    side: str
    price: float
    amount: float
```
Now if we try to enter wrong value in JSON to POST-method, for example int field "amount" set str type value:
```json
[
  {
    "id": 0,
    "user_id": 0,
    "currency": "string",
    "side": "string",
    "price": 0,
    "amount": ""
  }
]
```
We'll see such JSON-response:
```json
{
  "detail": [
    {
      "loc": [
        "body",
        0,
        "amount"
      ],
      "msg": "value is not a valid float",
      "type": "type_error.float"
    }
  ]
}
```
But if user enter negative price response will be given without errors to avoid this we should import Field and write smth like this:
```python
class Trade(BaseModel):
    """
    ge is >=
    le is <=
    """
    ...
    price: float = Field(ge=0)
    ...
```
Also we can write max_length to avoid long texts:
```python
class Trade(BaseModel):
    ...
    currency: str = Field(max_length=5)
    ...
```
To validate our response to web-server we should set response model argument in @app.get() func:
```python
class User(BaseModel):
    id: int
    role: str
    name: str


@app.get("/users/{user_id}", response_model=List[User])  # GET-request
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]
```
But that is not complicated structure like we will meet in real life, so in real life will be something like:
```python
from datetime import datetime
from enum import Enum
from typing import Optional, List


# Class representing all degrees that can be in degree list
class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


# Degree validation class
class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType

# Main data validation class
class User(BaseModel):
    id: int
    role: str
    name: str
    # Optional parameter for client if user for example don't have such a degree
    degree: Optional[List[Degree]] = [] 
```
And finally if we want to handle errors and response them to client we need to add such a structure:
```python
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError
from fastapi import status

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )
```
All code
```python
from datetime import datetime

from enum import Enum
from typing import List, Optional

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationError

from pydantic.fields import Field
from pydantic.main import BaseModel

# entry point to our web-app
app = FastAPI(
    title="Trading App"  # title
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )


# DB example:
fake_users = [
    {"id": 1, "role": "admin", "name": "Bob", "degree": [
        {"id": 1, "created_at": "2020-01-01T00:00:00", "type_degree": "expert"},
    ]},
    {"id": 2, "role": "investor", "name": "John", "degree": []},
    {"id": 3, "role": "trader", "name": "Matt", "degree": []},
]


class DegreeType(Enum):
    newbie = "newbie"
    expert = "expert"


class Degree(BaseModel):
    id: int
    created_at: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]]


@app.get("/users/{user_id}", response_model=List[User])  # GET-request
def get_user(user_id: int):
    return [user for user in fake_users if user.get("id") == user_id]

class Trade(BaseModel):
    """
    ge is >=
    le is <=
    """
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trade(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}
```
### 4. Data base and migrations<a name="fourth_lesson"></a>

First install sqlalchemy lib to work with sql db:

```commandline
pip install sqlalchemy
```

```commandline
pip install sqlalchemy alembic
```

Windows:
```commandline
pip install sqlalchemy alembic psycopg
```

Linux/Mac:
```commandline
pip install sqlalchemy alembic psycopg2-binary
```

Also we need to install postgresql and pgadmin4 to work with our database.

```commandline
sudo apt install postgresql postgresql-contrib
``` 

Install the public key for the repository (if not done previously):


```commandline
curl -fsS https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo gpg --dearmor -o /usr/share/keyrings/packages-pgadmin-org.gpg
```

Create the repository configuration file:


```commandline
sudo sh -c 'echo "deb [signed-by=/usr/share/keyrings/packages-pgadmin-org.gpg] https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
```
Install for both desktop and web modes:

```commandline
sudo apt install pgadmin4
```

To add database to pgadmin we have to create it via terminal

```commandline
sudo -i -u postgres
psql
createdb trading
ALTER USER postgres WITH PASSWORD 'postgres';
```
Open pgadmin4.

Register server:

![img](https://user-images.githubusercontent.com/65871712/236534772-cf74176d-f781-40c3-a155-b735e139581a.png)

Password: "postgres":

![img_1](https://user-images.githubusercontent.com/65871712/236534750-da932863-4b69-464b-80b5-3aae0d3f24b6.png)

Create directory and file *project*/models/models.py:

```python
from datetime import datetime

import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON


metaData = MetaData()

roles = Table(
    "roles",
    metaData,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)


users = Table(
    "users",
    metaData,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow()),
    Column("role_id", Integer, ForeignKey("roled.id")),
)


```

Initiate migrations using alembic:

*All migrations will be saved in /project/migrations/versions*

```commandline
alembic init migrations
```

In new alembic.ini file to hide out database data we'll change this string:

```ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```

To this:

```ini
sqlalchemy.url = postgresql://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s
```

Then we create .env file to write our hidden data:

```commandline
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
```

Then we create config.py file and write these:

```python
from dotenv import load_dotenv
import os


load_dotenv()

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
```

Then find /project/migrations/env.py file and write these imports:

```python
from config import DB_HOST, DB_PORT, DB_USER, DB_NAME, DB_PASS
```

Then after config init:

```python
# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config
```

We set our hidden data variables:

```python
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_HOST", DB_PORT)
config.set_section_option(section, "DB_HOST", DB_USER)
config.set_section_option(section, "DB_HOST", DB_NAME)
config.set_section_option(section, "DB_HOST", DB_PASS)
```

And change target_metadata variable to start work with our tables:

```python
from models.models import metaData

...

target_metadata = metaData
```

And finally to init our first migration we need to write smth like:

```commandline
alembic revision --autogenerate -m "Database creation"
```

In /project/migrations/versions will be created the migration file with two functions and four variables, 
all we need is value of revesion:

```python
revision = 'da2635964449'
```

To accept migration write next command:

```commandline
alembic upgrade da2635964449
```

Find our db named "postgres" in pgadmin4 and choose alembic_version to do the next query:

![img_2](https://user-images.githubusercontent.com/65871712/236534694-ca509ef4-bde8-4a07-af21-0d7be410ea1c.png)

Refresh tables and now we see 3 tables insted of 1. Well done!

![img_3](https://user-images.githubusercontent.com/65871712/236534669-466a06d6-3fdc-498b-a83f-3229a0c35f85.png)

---
