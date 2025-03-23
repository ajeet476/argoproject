# Build and publish images

Setup env
```shell
export PRJ=xx
export REPO=akt-io
```

```shell
echo asia-northeast1-docker.pkg.dev/$PRJ/$REPO
```

- Login

```shell
gcloud auth configure-docker \
    asia-northeast1-docker.pkg.dev
```

- Build and publish

```shell
docker-compose build
docker-compose push
```
