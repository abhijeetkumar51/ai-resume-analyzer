terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

resource "docker_network" "lab" {
  name = "resume-analyzer-devops-lab"
}

resource "docker_image" "app" {
  name         = "resume-analyzer-app:devops-lab"
  keep_locally = true

  build {
    context    = "${path.module}/.."
    dockerfile = "Dockerfile"
  }
}

resource "docker_image" "ansible_controller" {
  name         = "resume-analyzer-ansible:devops-lab"
  keep_locally = true

  build {
    context    = "${path.module}/../ansible"
    dockerfile = "Dockerfile"
  }
}

resource "docker_image" "monitoring" {
  name         = "resume-analyzer-monitoring:devops-lab"
  keep_locally = true

  build {
    context    = "${path.module}/.."
    dockerfile = "nagios/Dockerfile"
  }
}

resource "docker_container" "app" {
  name    = "resume-analyzer-app"
  image   = docker_image.app.image_id
  command = ["python", "app.py"]

  env = [
    "HOST=0.0.0.0",
    "PORT=5000",
  ]

  ports {
    internal = 5000
    external = 5000
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name    = docker_network.lab.name
    aliases = ["resume-analyzer-app"]
  }
}

resource "docker_container" "monitoring" {
  name    = "resume-analyzer-monitoring"
  image   = docker_image.monitoring.image_id
  command = ["sleep", "infinity"]

  ports {
    internal = 80
    external = 8080
    ip       = "127.0.0.1"
  }

  networks_advanced {
    name    = docker_network.lab.name
    aliases = ["resume-analyzer-monitoring"]
  }
}

resource "docker_container" "ansible_controller" {
  name    = "resume-analyzer-ansible"
  image   = docker_image.ansible_controller.image_id
  command = ["sleep", "infinity"]

  networks_advanced {
    name    = docker_network.lab.name
    aliases = ["resume-analyzer-ansible"]
  }

  volumes {
    host_path      = "/var/run/docker.sock"
    container_path = "/var/run/docker.sock"
    read_only      = true
  }
}

resource "terraform_data" "ansible_provisioning" {
  triggers_replace = [
    docker_container.app.id,
    docker_container.monitoring.id,
    docker_container.ansible_controller.id,
  ]

  provisioner "local-exec" {
    command = "docker exec ${docker_container.ansible_controller.name} ansible-playbook -i /playbooks/lab-inventory.yml /playbooks/configure-and-verify.yml"
  }
}

output "app_url" {
  description = "Local URL for the resume analyzer container."
  value       = "http://127.0.0.1:5000"
}

output "nagios_url" {
  description = "Local Nagios dashboard URL. Demo-only credentials are documented in the lab README."
  value       = "http://127.0.0.1:8080/nagios4/"
}
