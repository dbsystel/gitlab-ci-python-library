docker build -t gcip-embedme ./readme

docker run -v "$PWD":/work gcip-embedme
