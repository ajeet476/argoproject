# Stage 1: Use the argocd-extension-installer to download and install extensions
FROM quay.io/argoprojlabs/argocd-extension-installer:v0.0.8 as builder

# Hack
RUN echo "-k" > ~/.curlrc

# Install the Rollout extension
ENV EXTENSION_NAME=rollout-extension
ENV EXTENSION_URL=https://github.com/argoproj-labs/rollout-extension/releases/download/v0.3.4/extension.tar
RUN ./install.sh

# Install the Vault extension
RUN curl -Lf --max-time 30 https://github.com/argoproj-labs/argocd-vault-plugin/releases/download/v1.16.1/argocd-vault-plugin_1.16.1_linux_amd64 -o /tmp/extensions/argocd-vault-plugin && \  chmod +x /tmp/extensions/argocd-vault-plugin

# Stage 2: Use the official ArgoCD image as the base for the final image
FROM quay.io/argoproj/argocd:v2.13.2

# Copy the installed extensions from the builder stage to the final image
COPY --from=builder /tmp/extensions/ /usr/local/bin/
