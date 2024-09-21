# Step1: GKE Cluster

Create K8s cluster via GKE

setup context

```shell
export NS=dev-cpn
kubectl config set-context --current --namespace=$NA
```

# Step2: Install istio


# Step3: Install argocd

- Install argocd

https://argo-cd.readthedocs.io/en/stable/getting_started/

- Add ingress

```shell
kubectl apply -f argoprojects/argocd-ingress.yaml
```

Install CLI

# Step4: Deploy first app

Create helm chart

# Step4: xx


