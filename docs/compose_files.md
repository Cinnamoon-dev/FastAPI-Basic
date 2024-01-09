## Compose files
There are different compose files and each one of them serves one purpose.

### compose.test.yml
This is the compose file used for tests. It mirrors the current API folder in your PC, so every change made locally is transmitted to the container. It is useful because, this way, you get rid of systemwise variables.

#### Usage
Start the containers with the command below. Use `localhost:5000` to communicate with the containerized API.

```bash
$ docker compose -f compose.test.yaml up -d
```

Update the code inside the container by changing the files and then calling:

```bash
$ docker compose -f compose.test.yaml restart
```

Stop running the containers calling:

```bash
$ docker compose -f compose.test.yaml down
```

#### Database

It also creates a new database container that can be used instead of the local one and a backup of it in the folder `/docker/test-db-backup`. 

Use `sudo rm -rf ./docker/test-db-backup` to delete the backup. Look for `environment_variables.md` to choose what database you want to modify. 