## Environment variables
There are specific files used to provide environment variables to each service in the compose file. These files should be in the root level of the project.

### Database
The `.db.env` file provides the variables below to the database service:
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB

### API
The `.dev.env` file provides the variables below to the API service:
- POSTGRES_HOST
- POSTGRES_USER
- POSTGRES_PASSWORD
- POSTGRES_DB
- POSTGRES_PORT

`POSTGRES_HOST` should refer to the hostname property in the database service on the compose file.

```yaml
services:
    flask_db:
        hostname: flask_db
```

```
// .dev.env
POSTGRES_HOST=flask_db
```