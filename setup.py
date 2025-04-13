import subprocess
import sys
from dataclasses import dataclass

class NamespaceManager:
    def __init__(self, namespace):
        self.namespace = namespace

    def setup(self):
        print(f"Setting up namespace: {self.namespace}...")
        result = subprocess.run(
            f"kubectl get namespace {self.namespace}",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"Namespace '{self.namespace}' already exists.")
        else:
            print(f"Creating namespace '{self.namespace}'...")
            subprocess.run(
                f"kubectl create namespace {self.namespace}",
                shell=True, check=True
            )

    def switch(self):
        print(f"Switching to namespace {self.namespace}...")
        subprocess.run(
            f"kubectl config set-context --current --namespace={self.namespace}",
            shell=True, check=True
        )

    def delete(self):
        print(f"Deleting namespace '{self.namespace}' if it exists...")
        result = subprocess.run(
            f"kubectl get namespace {self.namespace}",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            subprocess.run(
                f"kubectl delete namespace {self.namespace}",
                shell=True, check=True
            )
            print(f"Namespace '{self.namespace}' deleted.")
        else:
            print(f"Namespace '{self.namespace}' not found. Skipping deletion.")

@dataclass
class WorkflowConfig:
    enable_istio: bool = True
    enable_istio_ingress: bool = True
    enable_argocd: bool = True

class AppWorkflow:

    def __init__(self, config: WorkflowConfig):
        self.config = config

    def run_command(self, command, shell=True, **kwargs):
        print(f"Executing: {command}")
        subprocess.run(command, shell=shell, check=True, **kwargs)

    def check_namespaces(self):
        print("Checking Kubernetes namespaces...")
        self.run_command(["kubectl", "get", "ns"], shell=False)

    def add_repo(self, repo, repo_url):
        print(f"Adding Helm repository: {repo}")
        self.run_command(f"helm repo add {repo} {repo_url}")
        self.run_command("helm repo update")

    def install_istio(self, namespace, values_path):
        print("Installing Istio...")
        self.add_repo("istio", "https://istio-release.storage.googleapis.com/charts")

        ns = NamespaceManager(namespace)
        ns.setup()
        ns.switch()

        self.install_or_upgrade_helm_release("istio-base", "istio/base", f"{values_path}/base.yaml", namespace)
        self.install_or_upgrade_helm_release("istiod", "istio/istiod", f"{values_path}/istiod.yaml", namespace, wait=True)

    def install_istio_ingress(self, namespace, values_path):
        print("Installing Istio Ingress Gateway...")
        ns = NamespaceManager(namespace)
        ns.setup()
        ns.switch()
        self.install_or_upgrade_helm_release("istio-ingress", "istio/gateway", f"{values_path}/ingress.yaml", namespace, wait=True)

    def install_argocd(self, namespace, values_path):
        print("Installing ArgoCD...")
        self.add_repo("argo", "https://argoproj.github.io/argo-helm")
        ns = NamespaceManager(namespace)
        ns.setup()

        self.install_or_upgrade_helm_release("argocd", "argo/argo-cd", f"{values_path}/argocd.yaml", namespace)
        self.install_or_upgrade_helm_release("argocd-rollouts", "argo/argo-rollouts", f"{values_path}/argocd-rollouts.yaml", namespace)

    def install_or_upgrade_helm_release(self, release_name, chart_name, values_file, namespace, wait=False):
        print(f"Checking if Helm release '{release_name}' exists in namespace '{namespace}'...")
        result = subprocess.run(
            f"helm list -n {namespace} | grep {release_name}",
            shell=True, capture_output=True, text=True
        )

        wait_flag = "--wait" if wait else ""
        action = "Upgrading" if result.returncode == 0 else "Installing"
        print(f"{action} Helm release '{release_name}'...")

        self.run_command(f"helm upgrade --install {release_name} {chart_name} -f {values_file} -n {namespace} {wait_flag}")

    def uninstall_helm_release(self, release_name, namespace):
        print(f"Uninstalling Helm release '{release_name}' from namespace '{namespace}'...")
        result = subprocess.run(
            f"helm list -n {namespace} | grep {release_name}",
            shell=True, capture_output=True, text=True
        )

        if result.returncode == 0:
            self.run_command(f"helm uninstall {release_name} -n {namespace}")
            print(f"'{release_name}' uninstalled.")
        else:
            print(f"'{release_name}' not found. Skipping...")

    def cleanup(self):
        print("Starting cleanup process...")

        # Uninstall releases
        self.uninstall_helm_release("istio-base", "istio-system")
        self.uninstall_helm_release("istiod", "istio-system")
        self.uninstall_helm_release("istio-ingress", "istio-ingress")
        self.uninstall_helm_release("argocd", "argocd")
        self.uninstall_helm_release("argocd-rollouts", "argocd")

        # Delete namespaces
        for ns in ["istio-system", "istio-ingress", "argocd"]:
            NamespaceManager(ns).delete()

        print("Cleanup complete.")

    def run(self):
        try:
            self.check_namespaces()

            if self.config.enable_istio:
                self.install_istio("istio-system", "applications/istio")

            if self.config.enable_istio_ingress:
                self.install_istio_ingress("istio-ingress", "applications/istio")

            if self.config.enable_argocd:
                self.install_argocd("argocd", "applications/argocd")

            print("Workflow completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Workflow failed: {e}")
            print("Output:", e.output or "No output")
            print("Error:", e.stderr or "No stderr")

if __name__ == "__main__":
    config = WorkflowConfig(
        enable_istio=True,
        enable_istio_ingress=True,
        enable_argocd=True
    )

    workflow = AppWorkflow(config)

    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        workflow.cleanup()
    else:
        workflow.run()
