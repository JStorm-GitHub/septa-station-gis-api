cp ../shared/api_key.txt .

docker build -t locust-test:latest .

docker run --rm --network="host" -p 8089:8089 -v "$(pwd):/locust/" locust-test:latest

rm -rf api_key.txt