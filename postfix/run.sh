
if [ "$1" ]; then
	DOCKER_NAME="--name $1"
fi

docker build -t shadowmail-postfix . && docker run --env-file env.list $DOCKER_NAME shadowmail-postfix
