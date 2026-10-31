# Puppet monitoring configuration

`modules/resume_analyzer_monitoring/manifests/init.pp` declares the monitoring node's desired state:

- Installs the Nagios HTTP-check plugin package.
- Renders a Nagios command, app host, and health-check service from `templates/resume-analyzer.cfg.erb`.
- Ensures Nagios and Apache are enabled and running after the configuration file is present.

The Ansible playbook runs `puppet apply` inside the Terraform-provisioned, disposable Linux monitoring container and then validates the resulting Nagios configuration. This is a real local configuration-management run; it does not configure Render's managed host. Apply the class only to a machine/container you control.
