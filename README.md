# FastAPI-Basic
## API Setup
The API relies on [poetry](https://python-poetry.org/docs/) to install the libraries needed for the application. It is recommended to use the following config:

```bash
$ poetry config virtualenvs.in-project true
```

Install the dependencies:

```bash
$ poetry install
```

Insert the needed mocked data:

```bash
$ python3 -m app.database.insertData
```

Source the virtualenv and run the project:

```bash
$ poetry shell # or $ source .venv/bin/activate
$ python3 main.py
```
## Database Setup
[Postgres](https://www.postgresql.org/download/) is the database used. Choose the database connection URL creating env variables specified in `/docs/environment_variables.md`. Alternatively, you can change the default values in the `app/database/__init__.py`.

```python
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL", "change_me_here")
SQLALCHEMY_DATABASE_TEST_URL = os.getenv("SQLALCHEMY_DATABASE_TEST_URL", "change_me_here")
STAGE = os.getenv("STAGE", "change_me_here")
```