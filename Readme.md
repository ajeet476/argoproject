# Step1: GKE Cluster

Create K8s cluster via GKE

# Step2: Install istio

```shell
istioctl install
```

# Step3: Setup namespace and gateway

see [docs](argoprojects/Readme.md)

## Setup context

```shell
export NS=dev-cpn
kubectl config set-context --current --namespace=$NS
```

# Step4: Install argocd

- Install argocd

https://argo-cd.readthedocs.io/en/stable/getting_started/

```shell
curl https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml | sed 's/namespace: argocd/namespace: cicd/g' > modified_install.yaml

kubectl apply -f modified_install.yaml
```


- Add ingress

```shell
kubectl apply -f argoprojects/argocd-ingress.yaml
```

Install CLI

# Step5: Deploy first app

Create helm chart

# Step6: xx
