# Command to build image and run to debug
docker build . -t {user}/eshop-notify
docker-compose up -d

# Command to build multi-architectur docker image
docker buildx build -t '{user}/eshop-notify' --platform linux/amd64,linux/arm/v7,linux/arm64 .

# Command to build multi-architecture docker image and deploy to dockerhub
docker buildx build -t '{user}/eshop-notify:{version}' -t '{user}/eshop-notify:latest' --platform linux/amd64,linux/arm/v7,linux/arm64 --push .
