## Environment variables
There are specific files used to provide environment variables to each service in the compose file. These files should be in the root level of the project.

You can also create these variables for you development environment in a `.env` file.

### Database
The `.db.env` file provides the variables below to the docker database service:
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

### API
The `.dev.env` file provides the variables below to the docker API service:
- POSTGRES_HOST
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_PORT

`POSTGRES_HOST` should refer to the hostname property in the database service on the compose file.

```yaml
services:
    fastapi_db:
        hostname: fastapi_db
```

```
// .dev.env
POSTGRES_HOST=fastapi_db
```

### Using the Database locally
There are three environment variables dedicated to the usage of the database for a local API:
- SQLALCHEMY_DATABASE_URL
- SQLALCHEMY_DATABASE_TEST_URL
- STAGE

`SQLALCHEMY_DATABASE_URL` defines the url used to connect to the database, if you want to connect to a test database use the variable `STAGE = 'test'` and `SQLALCHEMY_DATABASE_TEST_URL` to define the test database url.

`STAGE` variable should not be defined to any other value besides "test" if you are not going to use the test database, do not declare `STAGE`.

```
// .env
SQLALCHEMY_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastdb
SQLALCHEMY_DATABASE_TEST_URL=postgresql://postgres:postgres@localhost:5432/test_fastdb
STAGE=test
```