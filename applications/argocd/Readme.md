# Install argocd

Repo:
https://github.com/argoproj/argo-helm/tree/main/charts/argo-cd

```shell
helm repo add argo https://argoproj.github.io/argo-helm
```

Create Namespace

```shell
helm template argocd-ns helm-charts/namespace-common -f applications/namespace/argocd.yaml > tmp.yaml
kubectl apply -f tmp.yaml
```

```shell
# Argocd
helm install argocd argo/argo-cd -f argocd.yaml

# Argo-rollout
helm install argocd-rollouts argo/argo-rollouts -f argocd-rollouts.yaml
```

# Install Main App

Create `main.yaml` manually
