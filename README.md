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

Source the virtualenv and run the project:

```bash
$ poetry shell # or $ source .venv/bin/activate
$ python3 main.py
```
## Database Setup
[Postgres](https://www.postgresql.org/download/) is the database used. Choose the database connection URL creating env variables specified in `/docs/environment_variables.md`. Alternatively, you can change the default values in the `app/database/__init__.py`.

```python
USER = os.getenv("POSTGRES_USER", "change_me_here")
PASSWORD = os.getenv("POSTGRES_PASSWORD", "change_me_here")
HOST = os.getenv("POSTGRES_HOST", "change_me_here")
PORT = os.getenv("POSTGRES_PORT", "change_me_here")
DATABASE = os.getenv("POSTGRES_DB", "change_me_here")
TEST_DATABASE = os.getenv("TEST_POSTGRES_DB", "change_me_here")
```