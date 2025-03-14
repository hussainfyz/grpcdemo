import os
import subprocess
import json
import time
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load config.json
CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from config.json"""
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error loading configuration: {e}")
        exit(1)

def run_command(command, check_output=False):
    """Run a shell command and log output"""
    try:
        if check_output:
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            logging.info(result.strip())
            return result.strip()
        else:
            subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {command}")
        logging.error(e.output if check_output else e)
        exit(1)

def docker_login(username, password):
    """Login to Docker Hub"""
    logging.info("Logging into Docker Hub...")
    run_command(f"echo '{password}' | docker login -u '{username}' --password-stdin")

def build_and_push_docker_image(service_name, repo):
    """Build and push Docker image"""
    logging.info(f"Building Docker image {repo}:latest...")
    run_command(f"docker build -t --no-cache {repo}:latest -f Dockerfile .")
    logging.info(f"Pushing Docker image {repo}:latest to Docker Hub...")
    run_command(f"docker push {repo}:latest")

def deploy_openshift(service_name, oc_cluster, repo, port):
    """Deploy application on OpenShift"""
    logging.info(f"Deleting existing app {service_name} (if any)...")
    os.system(f"oc delete all -l app={service_name} --ignore-not-found=true")
    time.sleep(5)

    logging.info(f"Deploying {repo} on OpenShift...")
    run_command(f"oc new-app {repo}:latest --name=grpc --as-deployment-config")
    
    logging.info(f"Exposing {service_name} service on port {port}...")
    run_command(f"oc expose svc/{service_name} --port={port}")

    logging.info("Forcing OpenShift to update the image...")
    os.system(f"oc tag --source=docker {repo}:latest {service_name}:latest --force")
    
    logging.info("Restarting deployment to apply new image...")
    os.system(f"oc rollout restart dc/{service_name}")

def main():
    """Main deployment process"""
    logging.info("Starting deployment process...")
    config = load_config()

    docker_username = config["docker_username"]
    docker_password = config["docker_password"]
    docker_repo = config["docker_repo"]

    services = [
        {"name": "grpc", "port": 50051}
    ]

    # Docker Login
    docker_login(docker_username, docker_password)

    for service in services:
        build_and_push_docker_image(service["name"], docker_repo)
        deploy_openshift(service["name"], config["oc_cluster"], docker_repo, service["port"])

    logging.info("Deployment complete!")

if __name__ == "__main__":
    main()
