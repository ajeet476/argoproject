import subprocess
import sys

class AppWorkflow:

    def check_namespaces(self):
        print("Checking Kubernetes namespaces...")
        subprocess.run(["kubectl", "get", "ns"], check=True)

    def add_repo(self, repo, repo_url):
        print(f"Adding Helm repository: {repo} ...")
        subprocess.run(f"helm repo add {repo} {repo_url}", shell=True, check=True)
        subprocess.run("helm repo update", shell=True, check=True)

    def install_istio(self, namespace, values_path):
        print("Installing Istio using Helm...")
        self.add_repo("istio", "https://istio-release.storage.googleapis.com/charts")
        self.setup_namespace(namespace)
        self.switch_namespace(namespace)

        self.install_or_upgrade_helm_release("istio-base", "istio/base", f"{values_path}/base.yaml", namespace)
        self.install_or_upgrade_helm_release("istiod", "istio/istiod", f"{values_path}/istiod.yaml", namespace, wait=True)

    def install_istio_ingress(self, namespace, values_path):
        self.setup_namespace(namespace)
        self.switch_namespace(namespace)
        self.install_or_upgrade_helm_release("istio-ingress", "istio/gateway", f"{values_path}/ingress.yaml", namespace, wait=True)

    def install_argocd(self, values_path):
        print("Installing ArgoCD...")
        self.add_repo("argo", "https://argoproj.github.io/argo-helm")

        self.setup_namespace("argocd")

        self.install_or_upgrade_helm_release("argocd", "argo/argo-cd", f"{values_path}/argocd.yaml", "argocd")
        self.install_or_upgrade_helm_release("argocd-rollouts", "argo/argo-rollouts", f"{values_path}/argocd-rollouts.yaml", "argocd")

    def setup_namespace(self, namespace):
        print(f"Setting up namespace: {namespace}...")
        result = subprocess.run(f"kubectl get namespace {namespace}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Namespace '{namespace}' already exists. Skipping creation.")
        else:
            print(f"Creating namespace '{namespace}'...")
            subprocess.run(f"kubectl create namespace {namespace}", shell=True, check=True)

    def switch_namespace(self, namespace):
        print(f"Switching to namespace {namespace}...")
        subprocess.run(f"kubectl config set-context --current --namespace={namespace}", shell=True, check=True)

    def install_or_upgrade_helm_release(self, release_name, chart_name, values_file, namespace, wait=False):
        """Installs or upgrades a Helm release in the given namespace."""
        print(f"Checking if Helm release '{release_name}' exists in namespace '{namespace}'...")

        result = subprocess.run(f"helm list -n {namespace} | grep {release_name}", shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Helm release '{release_name}' already exists. Upgrading...")
        else:
            print(f"Installing Helm release '{release_name}'...")

        wait_flag = "--wait" if wait else ""
        subprocess.run(f"helm upgrade --install {release_name} {chart_name} -f {values_file} -n {namespace} {wait_flag}", shell=True, check=True)

    def uninstall_helm_release(self, release_name, namespace):
        """Uninstalls a Helm release if it exists."""
        print(f"Uninstalling Helm release '{release_name}' in namespace '{namespace}'...")

        result = subprocess.run(f"helm list -n {namespace} | grep {release_name}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.run(f"helm uninstall {release_name} -n {namespace}", shell=True, check=True)
            print(f"Helm release '{release_name}' has been uninstalled.")
        else:
            print(f"Helm release '{release_name}' not found in namespace '{namespace}', skipping.")

    def delete_namespace(self, namespace):
        """Deletes a namespace if it exists."""
        print(f"Deleting namespace '{namespace}' if it exists...")
        result = subprocess.run(f"kubectl get namespace {namespace}", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.run(f"kubectl delete namespace {namespace}", shell=True, check=True)
            print(f"Namespace '{namespace}' deleted.")
        else:
            print(f"Namespace '{namespace}' not found, skipping deletion.")

    def cleanup(self):
        """Uninstalls all Helm releases and deletes their namespaces."""
        print("Starting cleanup process...")

        # Uninstall Istio
        self.uninstall_helm_release("istio-base", "istio-system")
        self.uninstall_helm_release("istiod", "istio-system")
        self.uninstall_helm_release("istio-ingress", "istio-system")

        # Uninstall ArgoCD
        self.uninstall_helm_release("argocd", "argocd")
        self.uninstall_helm_release("argocd-rollouts", "argocd")

        # Delete namespaces
        self.delete_namespace("istio-system")
        self.delete_namespace("argocd")

        print("Cleanup process completed successfully.")

    def run(self):
        try:
            self.check_namespaces()
            self.install_istio("istio-system", "applications/istio")
            self.install_istio_ingress("istio-ingress", "applications/istio")
            self.install_argocd("applications/argocd")
            print("Workflow completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred during the workflow: {e}")
            print("Command output:", e.output if e.output else "No output")
            print("Command error:", e.stderr if e.stderr else "No error details")

if __name__ == "__main__":
    workflow = AppWorkflow()

    if len(sys.argv) > 1 and sys.argv[1] == "cleanup":
        workflow.cleanup()
    else:
        workflow.run()
