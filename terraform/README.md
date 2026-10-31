# Terraform local DevOps lab

`main.tf` uses the Docker provider to build the application, Ansible-controller, and monitoring images; create an isolated bridge network; and launch the app, Puppet/Nagios monitoring node, and Ansible controller. Terraform then invokes Ansible. The playbook applies the Puppet module in the monitoring container, validates and restarts Nagios/Apache, and asserts the app health endpoint.

## Prerequisites

- Docker Desktop running with the **Linux container** engine.
- Terraform 1.5 or later.
- Docker CLI available on `PATH`.
- The controller mounts `/var/run/docker.sock`; this grants Docker API control comparable to root on the local Docker host. Use only on a trusted, disposable local machine. Do not expose this controller or its socket on a shared or production host.

## Run and verify

From the repository root:

```powershell
$env:DOCKER_HOST = 'npipe:////./pipe/dockerDesktopLinuxEngine'
docker info
terraform -chdir=terraform init
terraform -chdir=terraform fmt -check
terraform -chdir=terraform validate
terraform -chdir=terraform apply
```

The Docker provider uses `DOCKER_HOST` directly and does not resolve Docker Desktop's named context automatically. On Linux, set `DOCKER_HOST=unix:///var/run/docker.sock` instead.

Terraform outputs the app URL (`http://127.0.0.1:5000`) and the local Nagios dashboard (`http://127.0.0.1:8080/nagios4/`). The dashboard credentials are `nagiosadmin` / `devops-demo` and are for this loopback-only demonstration only. The Nagios service check may take one or two intervals to show its first result.

Check the app directly at `http://127.0.0.1:5000/health`. Terraform's Ansible provisioner also fails the apply if the app health assertion or Nagios configuration validation fails.

## Cleanup

```powershell
terraform -chdir=terraform destroy
```

The local lab is separate from the Render deployment. Render's managed service does not expose its host for Terraform, Puppet, or Nagios configuration; `render.yaml` remains the Render Blueprint. Terraform state and provider files are local and must not be committed.
