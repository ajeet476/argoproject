# Namespace

Common

```shell
# cicd
helm template cicd helm-tmpl -f namespace/cicd.yaml

# middleware
helm template middleware helm-tmpl -f namespace/middleware.yaml
```

Apps
```shell
# DEV
helm template dev helm-tmpl -f namespace/dev.yaml

# DEV
helm template stg helm-tmpl -f namespace/stg.yaml
```


# Apps

## App: Use API

```shell
helm template use helm-tmpl -f apps/use-api.yaml
```

## App: Aq API

```shell
helm template use helm-tmpl -f apps/aq-api.yaml
```
