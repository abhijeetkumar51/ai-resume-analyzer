terraform {
  required_version = ">= 1.5.0"
}

# Render web service configuration lives in render.yaml. Render does not expose
# the service's underlying host for Terraform, Ansible, Puppet, or Nagios access.
# Add Terraform resources here only for external infrastructure you own, such as
# DNS, a monitoring VM, or an alerting service. Keep credentials in environment
# variables or a secrets manager; never commit them.
