import os
import subprocess
import json
import logging
import shutil

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load config.json
CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from config.json"""
    try:
        with open(CONFIG_FILE, "r") as file:
            config = json.load(file)
        return config
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
    run_command(f"docker build -t {repo}:latest -f Dockerfile .")
    #run_command(f"docker tag {repo} myuser/myrepo:latest")
    logging.info(f"Pushing Docker image {repo}:latest to Docker Hub...")

    run_command(f"docker push {repo}:latest")

def deploy_openshift(service_name, oc_cluster, repo, port, protocol):
    """Deploy application on OpenShift"""
    logging.info(f"Deploying {service_name} on OpenShift...")
    run_command(f"oc new-app {repo}:latest --name={service_name} || oc rollout restart deployment/{service_name}")
    logging.info(f"Exposing {service_name} service...")
    run_command(f"oc expose svc/{service_name} --port={port}")

def main():
    """Main deployment process"""
    logging.info("Starting deployment process...")
    config = load_config()

    docker_username = config["docker_username"]
    docker_password = config["docker_password"]
    docker_repo = config["docker_repo"]
    oc_cluster = config["oc_cluster"]

    services = [
    
         {"name": "grpc", "port": 50051, "protocol": "TCP"}
    ]

    # Docker Login
    docker_login(docker_username, docker_password)

    for service in services:
        build_and_push_docker_image(service["name"], docker_repo)
        deploy_openshift(service["name"], oc_cluster, docker_repo, service["port"], service["protocol"])

    logging.info("Deployment complete!")

if __name__ == "__main__":
    main()
