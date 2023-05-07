# FastAPI-course

## Navigation:


##### 1. [Installation and start](#first_lesson)
* 1.1.  [Documentation and site adress](#doc)
##### 2. [Endpoints](#second_lesson)
* 2.1. [GET-method by id(Primary Key)](#by_id)
* 2.2. [GET-method by query-parameters](#query)
* 2.3. [POST-method to change username](#post)
##### 3. [Data Validation](#third_lesson)
* 3.1. [Using of 'response_model' argument in GET-method](#response_model)
* 3.2. [Handling of errors](#handling_of_errors)
##### 4. [Data base and migrations](#fourth_lesson)
* 4.1. [Installation postgresql and pgadmin4](#installation)
* 4.2. [Configure server via postgresql and pgadmin4](#conf_pg)
* 4.3. [Create models](#create_models)
* 4.4. [Metadata](#metadata)
* 4.5. [Migrations and connect to database in FastAPI project.](#migrations_and_connect)
##### 5. [Registration and authorization users](#fivth_lesson)
* 5.1. [Authentication Backend](#auth)
* 5.2. [Cookie + JWT](#cookie+jwt)
* 5.3. [UserManager](#usermanager)
* 5.4. [Schemas](#schemas)
* 5.5. [Routers](#routers)
* 5.6. [Roles customization](#roles)
* 5.7. [Registration, login and JWT-token inside cookie](#reg_log)
* 5.8. [Protected endpoint](#protected_endpoint)
##### 6. [Routers and file structure](#routers_and_files)
* 6.1. [Router. What is it?](#router)
* 6.2. [SQL-injection and ORM](#sql_ORM)
##### 7. [Project design](#project_design)

## Lessons:


### 1. Installation and start<a name = "first_lesson"></a>:

Cd ***project_root*** 
for e.g.:
```commandline
cd /home/bogdan/PycharmProjects/FastAPI-course
```

Create "filename".py (for e.g.: main.py)

Write in terminal these commands:

```commandline
python -m venv venv
```
```commandline
source venv/bin/activate
```
```commandline
pip install fastapi[all]
```

Write this code in file:

```python
from fastapi import FastAPI

app = FastAPI()     # entry point to our web-app


@app.get("/")   # GET-request
def hello():
    return "Hello world!"
```

To start write this in terminal:

```commandline
uvicorn main:app --reload
```
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
<a name = "by_id"></a>
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
<a name = "query"></a>
Write GET-method with query-parameters to return trades with pagination
```python
@app.get("/trades")
def get_trades(limit: int = 10, offset: int = 10):
    return fake_trades[offset:][:limit]
```
* limit - trades limit
* pagination - number of trades on one page

<a name = "post"></a>
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
<a name = "response_model"></a>
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
<a name = "handling_of_errors"></a>
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
### 4. Database and migrations. <a name="fourth_lesson"></a>
<a name = "installation"></a>
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
<a name = "conf_pg"></a>
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

<a name = "create_models"></a>
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

<a name = 'metadata'></a>
> The metadata variable accumulates information about the created tables, after which they are processed by alembic and compared with the real situation in the database

<a name="migrations_and_connect"></a>

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
from auth.models import metaData

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

### 5. Registration and authorization users<a name="fivth_lesson"></a>

Let's look at ways of keeping token:

![img](https://user-images.githubusercontent.com/65871712/236630974-7a6b9150-c860-407f-a018-58b3b345bec3.png)

All we need to know is:

> User model - our database table
>
> SQLAchemy/Beanie - adapters

> UserManager - class to managing users settings(to manage his data)

> get_user_manager - function that returns UserManager

Authentication:

> Transport:
> 
> CookieTransport - Cookie storage is used to transport our token

> Strategies:
> JWTStrategy - token is kept inside our users browser


<a name = "auth"></a>
Install fastapi-users:
```commandline
pip install 'fastapi-users[sqlalchemy]'
```

Install async driver:
```commandline
pip install asyncpg
```

Then we create /project/auth/database.py file and paste there this code:
 
```python
from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from datetime import datetime

from sqlalchemy import String, Boolean, Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTable, Base):
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    username: Mapped[str] = mapped_column(
        String, nullable=False
    )
    registered_at: Mapped[datetime] = mapped_column(
        TIMESTAMP, default=datetime.utcnow()
    )
    role_id: Mapped[int] = mapped_column(
        Integer, ForeignKey(role.c.id)
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(length=1024), nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, nullable=False
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )


engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
```

Delete our tables users and roles and change models.py file in a such way:

```python
from datetime import datetime

import sqlalchemy
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean


metaData = MetaData()

role = Table(
    "role",
    metaData,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)


user = Table(
    "user",
    metaData,
    Column("id", Integer, primary_key=True),
    Column("email", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow()),
    Column("role_id", Integer, ForeignKey(role.c.id)),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),
)
```

Then do migrations:

```commandline
alembic revision --autogenerate -m "Initial"
alembic upgrade head
```

After that we can delete these strokes from database.py file:

```python
async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```
Because our tables has been created already!

In FastAPI there is such an interesting function called Depends and we are already using it in our database.py.
To understand why we need this func and why in follows main principe of programming
DRY(Don't Repeat Yourself) we'll change our main.py file.

```python
from typing import Annotated

from fastapi import FastAPI, Depends


# entry point to our web-app
app = FastAPI(
    title="Trading App"  # title
)


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
```

And 
```commandline
uvicorn main:app --reload
```

We'll see that parameters from the first func will be all other funcs where we set Depends func and give inside of it 
as argument name of func from which we want to take our parameters.

![img_1](https://user-images.githubusercontent.com/65871712/236631004-3d3c0238-2af7-4ad6-9182-fa16a189acd7.png)

<a name = "cookie+jwt"></a>
To set cookie storage and JWT we have to create auth.py file in /project/auth/auth.py:

```python
from fastapi_users.authentication import CookieTransport
from fastapi_users.authentication import JWTStrategy


cookie_transport = CookieTransport(cookie_name="bonds ", cookie_max_age=3600)


SECRET = 'SECRET'


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600
```
<a name = "usermanager"></a>

Create /project/auth/manage.py:

```python
import uuid
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from database import User, get_user_db

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
```

<a name = "schemas"></a>
Create /project/auth/schemas.py:

```python
from typing import Optional

from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


```
<a name = "routers"></a>
Router is a variable that contains ednpoints.
In main.py file add:

```python
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from src.auth.base_config import auth_backend
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from database import User

app = FastAPI(
    title="Trading App"  # title
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
```

And in documentation we'll see:
![img_2](https://user-images.githubusercontent.com/65871712/236631035-c6938944-52db-49c1-a8f4-ee2350f152fb.png)

<a name = "roles"></a>
Next step is to create roles in role table inside pgadmin using query tools:
```
INSERT INTO role VALUES (1, 'user', null), (2, 'admin', null);
```

And we'll change our manage.py file to correct choosing of role when user was resistered:

```python
from typing import Optional

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin, models, exceptions, schemas

from database import User, get_user_db

SECRET = "SECRET"


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        """
        Create a user in database.

        Triggers the on_after_register handler on success.

        :param user_create: The UserCreate model to create.
        :param safe: If True, sensitive values like is_superuser or is_verified
        will be ignored during the creation, defaults to False.
        :param request: Optional FastAPI request that
        triggered the operation, defaults to None.
        :raises UserAlreadyExists: A user already exists with the same e-mail.
        :return: A new user.
        """
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
```

<a name = "reg_log"></a>
Now when we are gonna try to register user we'll succesfully do this:

![img_3](https://user-images.githubusercontent.com/65871712/236631045-d48c962a-d08d-4017-9532-b4966d145758.png)
![img_4](https://user-images.githubusercontent.com/65871712/236631049-31721d54-cd6b-45c9-91a7-ba0ad596a3de.png)
![img_5](https://user-images.githubusercontent.com/65871712/236631052-372d61a1-234c-4746-b520-f44874cebdba.png)

Now when we'll try to login we'll see such a cookie after successful login:
![img_7](https://user-images.githubusercontent.com/65871712/236631059-46be7395-c501-4fc9-8221-62db059d0bb6.png)
![img_6](https://user-images.githubusercontent.com/65871712/236631056-b27566b8-a368-4aae-adb4-97260dc6cd3d.png)

<a name = "protected_endpoint"></a>
We'll add inside of our main.py file two GET-methods:

```python
@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"

current_user = fastapi_users.current_user()

@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonim"
```

And test them to see difference:

![img_8](https://user-images.githubusercontent.com/65871712/236631065-2edf403d-c0f7-4af1-ae08-d4d7998e8711.png)
![img_9](https://user-images.githubusercontent.com/65871712/236631068-cd527480-a8b4-4bcd-89d1-8759b6338884.png)

But if we delete cookie we'll see:

![img_10](https://user-images.githubusercontent.com/65871712/236631075-8a4b22c9-acbd-4f59-b56d-38ef89d2412c.png)
![img_11](https://user-images.githubusercontent.com/65871712/236631079-5ff78022-0791-44c0-bc33-4a66b2c4301f.png)

### 6. Routers and file structure.<a name = "routers_and_files"></a>
![img.png](img.png)

Best practice:

![img_1.png](img_1.png)

Refactoring our [code](https://github.com/socloseeee/FastAPI-course/tree/b0ed65545297c2938137c9cf964a04d842cab860)

<a name = "router"></a>
Router includes group of endpoints:

```python
from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate

router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
```

And then imports into main.py file:

```python
from fastapi import FastAPI
from operations.router import router as router_operation

# entry point to our web-app
app = FastAPI(
    title="Trading App"  # title
)

...

app.include_router(router_operation)

```

<a name = "sql_ORM"></a>
To avoid SQL-Injection we have to write not-RAW SQL-querys using ORM, for example:

```python
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
```

Why do we need commit in main.py files post-method?

```python
@router.post("/")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
```

In order to update the information simultaneously in several tables, or nothing was recorded. By the atomicity property.
<a name = "project_design"></a>
### 7. Project design.

---
