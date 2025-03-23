# Chart

This chart generate base project via [argoapp](../../applications/argocd/main.yaml)

## Why do we have files/**.yaml

Due to
https://github.com/helm/helm/issues/2798

ApplicationSet template and Helm Template are in conflicts, so we need to prevent HELM
