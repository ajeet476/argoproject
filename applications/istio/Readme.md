# Install

## Using istioctl

```shell
istioctl install
```

- when using gateway API

```shell
# check
kubectl get crd gateways.gateway.networking.k8s.io
# if not exits
kubectl kustomize "github.com/kubernetes-sigs/gateway-api/config/crd?ref=v1.1.0" | kubectl apply -f -

# install istio
istioctl install --set profile=minimal -y
```

## Using Helm

```shell
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm repo update
```

install helm charts
```shell
kubectl create namespace istio-system
helm install istio-base istio/base -f base.yaml -n istio-system
helm install istiod istio/istiod -f istiod.yaml --wait -n istio-system
```

```shell
kubectl create namespace istio-ingress
helm install istio-ingress istio/gateway -f ingress.yaml --wait
```
