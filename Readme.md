# Step0: clone repo and setup

```shell
git clone https://github.com/ajeet476/argoproject.git

# check namespaces
kubectl get ns
```

# Step1: GKE Cluster

Create K8s cluster via GKE

# Step2: Install istio

Using Helm: [see](applications/middleware/istio/Readme.md)

# Step3: Setup namespace and gateway

see [docs](applications/Readme.md)

## Setup context

```shell
export NS=argocd
kubectl config set-context --current --namespace=$NS
```


## Utils

```shell
pip3 install pyyaml --break-system-packages
```

```shell
python3 deploy.py debug
```
