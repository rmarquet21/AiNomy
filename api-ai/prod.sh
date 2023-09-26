export DOCKER_DEFAULT_PLATFORM=linux/amd64

docker-compose -f ./docker/docker-compose.yml -p ainomy up -d --build
