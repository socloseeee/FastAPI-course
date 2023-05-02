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
### 4. Data base and migrations

---
