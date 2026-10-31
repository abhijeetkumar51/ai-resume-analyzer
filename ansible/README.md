# Ansible automation

`playbooks/check-render-health.yml` checks the public Render endpoint after setting `SERVICE_URL=https://your-service.onrender.com`.

The local DevOps lab uses `playbooks/configure-and-verify.yml`. Terraform creates the Docker network and containers, then runs this playbook in the Ansible controller container. The controller image includes the Docker CLI, Python Docker SDK, `ansible-core`, and the `community.docker` collection. The `community.docker.docker` connection plugin uses the Docker socket to apply the Puppet manifest inside the monitoring container, validate and restart Nagios, and check the application health endpoint. This is a local lab integration, not host access to Render.

Run the end-to-end workflow from the repository root with `terraform -chdir=terraform init` followed by `terraform -chdir=terraform apply`. See `README.md` for prerequisites, teardown, and Docker socket security.
