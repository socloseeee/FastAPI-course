# FastAPI-course

### Navigation:

##### 1. [Installation and start](#first_lesson)
##### 2. [Endpoints](#second_lesson)

### Lessons:

#### 1. Installation and start<a name = "first_lesson"></a>:

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

Site will run on localhost: http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs#/default

Redoc: http://127.0.0.1:8000/redoc

#### 2. Endpoints<a name = "second_lesson"></a>:

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

Write combined POST-method:
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
