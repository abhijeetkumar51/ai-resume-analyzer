# Ansible starter

Run `ansible-playbook playbooks/check-render-health.yml` after setting `SERVICE_URL=https://your-service.onrender.com`. This checks the public HTTP endpoint from your machine or CI runner. It does not connect to a Render host. Requires Ansible Core with the built-in `uri` module.
