Need to make a build such that the directories are aligned like:

# Development

This uses docker compose as a development environment.

## Requirements

1. Docker
2. docker-compose
3. Jekyll: https://jekyllrb.com/docs/installation/

Instructions can be found on Docker's website, https://docs.docker.com/compose/gettingstarted/

## Running

### Python Virtual Environment
Create a python virtual environment in which to install dependencies and from which scripts will be called.

```
python3 -m venv env
```

The name `env` is important as that is the directory that will be used by docker-compose in the environment.

### Run Docker

To start apache and the mysql server in docker, from the top directory (`eric-off-the-rails`):

```
docker-compose up --build
```

This will build the docker images and then run the container with the proper volume mounts and start apache pointed to the Jekyll site on the host machine.

### Run Jekyll

In the `static` directory, run:

```
bundle exec jekyll build -w
```

The `-w` option tell jekyll to watch for source file changes and will rebuild the site into the `_site` directory. This is then served by apache in the docker container.
