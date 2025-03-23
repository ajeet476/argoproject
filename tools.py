import subprocess

def run_command(command, description=""):
    """Run a shell command and handle errors."""
    print(f"🔹 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} - Done")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description} failed\n{e}")

def install_k9s():
    """Install k9s in Google Cloud Shell."""
    run_command("curl -sS https://webinstall.dev/k9s | bash", "Installing k9s")
    # run_command("sudo mv ~/.local/bin/k9s /usr/local/bin/", "Moving k9s to /usr/local/bin")

def install_gcloud_tools():
    """Ensure Google Cloud CLI tools are installed."""
    run_command("gcloud --version", "Checking gcloud CLI")
    run_command("kubectl version --client", "Checking kubectl")
    run_command("helm version", "Checking Helm")

    # Install missing tools
    #run_command("gcloud components install kubectl", "Installing kubectl via gcloud")
    #run_command("curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash", "Installing Helm")

def configure_gke_cluster(cluster_name, region):
    """Configure and authenticate with a GKE cluster."""
    command = f"gcloud container clusters get-credentials {cluster_name} --region {region}"
    run_command(command, f"Configuring GKE cluster {cluster_name}")

def main():
    """Main function to install tools and configure GKE."""
    print("🚀 Starting GKE Tools Setup...\n")

    install_gcloud_tools()
    install_k9s()

    cluster_name = input("Enter your GKE cluster name: ")
    region = input("Enter your GKE cluster region: ")

    configure_gke_cluster(cluster_name, region)

    print("\n✅ All tools installed successfully! Run `k9s` to start.")

if __name__ == "__main__":
    main()
