# Step1: GKE Cluster

Create K8s cluster via GKE

setup context

```shell
export NS=dev-cpn
kubectl config set-context --current --namespace=$NA
```

# Step2: Install istio

```shell
istioctl install
```

# Step3: Setup namespace and gateway

see [docs](argoprojects/Readme.md)

# Step4: Install argocd

- Install argocd

https://argo-cd.readthedocs.io/en/stable/getting_started/

kubectl apply -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml


- Add ingress

```shell
kubectl apply -f argoprojects/argocd-ingress.yaml
```

Install CLI

# Step5: Deploy first app

Create helm chart

# Step6: xx
