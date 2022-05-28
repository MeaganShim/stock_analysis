#!/bin/bash

CONTAINER="stock_analysis"
echo "Starting Container $CONTAINER"

docker rm -vf $CONTAINER
docker buildx build --platform linux/amd64 -t $CONTAINER .
docker run --platform linux/amd64 -t --name $CONTAINER $CONTAINER "$@"