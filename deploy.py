import os
import subprocess
import sys
import yaml
import glob

class HelmAppManager:
    def __init__(self):
        """Initialize HelmAppManager with detected applications."""
        self.app_configs = self.find_apps()
        self.tmp_dir = "tmp"
        os.makedirs(self.tmp_dir, exist_ok=True)  # Ensure tmp directory exists

    def find_apps(self):
        """Find all `app_global.yaml` files in `applications/**/` and parse them."""
        app_configs = []
        for filepath in glob.glob("applications/**/app_global.yaml", recursive=True):
            with open(filepath, "r") as file:
                try:
                    config = yaml.safe_load(file)
                    if config:
                        app_configs.append({
                            "release_name": os.path.basename(os.path.dirname(filepath)),
                            "chart_path": config.get("chart_path", "helm-charts/app"),  # Default to local chart
                            "namespace": config.get("namespace", "default"),
                        })
                except yaml.YAMLError as e:
                    print(f"❌ Failed to parse {filepath}: {e}")
        return app_configs

    def run_command(self, command):
        """Executes a shell command and handles errors."""
        try:
            subprocess.run(command, shell=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Error executing command: {command}")
            print(f"🔴 Error message: {e}")
            sys.exit(1)

    def install(self):
        """Installs all detected applications using Helm."""
        if not self.app_configs:
            print("⚠️ No applications found for installation.")
            return

        for app in self.app_configs:
            print(f"🚀 Installing {app}...")
            self.run_command(f"helm install {app['release_name']} {app['chart_path']} -n {app['namespace']} --create-namespace")
            print(f"✅ {app['release_name']} installed successfully!")

    def uninstall(self):
        """Uninstalls all detected applications."""
        if not self.app_configs:
            print("⚠️ No applications found for uninstallation.")
            return

        for app in self.app_configs:
            print(f"🗑️ Uninstalling {app['release_name']}...")
            self.run_command(f"helm uninstall {app['release_name']} -n {app['namespace']}")
            print(f"✅ {app['release_name']} uninstalled successfully!")

    def debug_templates(self):
        """Renders Helm templates and writes them to a file in tmp/template.yaml."""
        if not self.app_configs:
            print("⚠️ No applications found for debugging.")
            return

        for app in self.app_configs:
            app_name = app['release_name']
            app_values = []
            for filepath in glob.glob(f"applications/{app_name}/app_*.yaml", recursive=True):
                app_values.append(filepath)
            print(f"📝 Rendering Helm template for {app}... with {app_values}")

            values_files = " ".join(f"-f {item}" for item in app_values)
            # Run Helm template command and capture output
            result = subprocess.run(
                f"helm template {app_name} {app['chart_path']} -n {app['namespace']} {values_files} --debug",
                shell=True, capture_output=True, text=True
            )

            if result.returncode == 0:
                with open(os.path.join(self.tmp_dir, f"{app_name}.yaml"), "w") as f:
                    f.write(result.stdout + "\n")
                print(f"✅ Template written for {app['release_name']}")
            else:
                print(f"❌ Failed to render template for {app['release_name']}")
                print(f"🔴 Error: {result.stderr}")

        print(f"📄 All templates saved to tmp")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Please specify 'install', 'uninstall', or 'debug'.")
        sys.exit(1)

    manager = HelmAppManager()

    if sys.argv[1] == "install":
        manager.install()
    elif sys.argv[1] == "uninstall":
        manager.uninstall()
    elif sys.argv[1] == "debug":
        manager.debug_templates()
    else:
        print("❌ Invalid command! Use 'install', 'uninstall', or 'debug'.")
