# Nagios monitoring

The local lab builds this Nagios image from `Dockerfile`. Ansible applies the Puppet-managed object configuration, validates it with `nagios4 -v`, and starts Nagios Core plus Apache. The configured service uses the standard `check_http` plugin to poll the app's `/health` endpoint over the isolated Docker network. Nagios checks every minute, retries every minute, and marks a service warning/critical above 5/10 seconds.

Open `http://127.0.0.1:8080/nagios4/` after `terraform -chdir=terraform apply`. Local demo credentials: `nagiosadmin` / `devops-demo`. This intentionally loopback-only demo credential must never be reused on a public host.

`commands.cfg` and `services.cfg` remain examples for configuring a separately administered Nagios server to check a public Render URL. Replace the placeholder hostname and validate/reload that server's configuration before use. Render does not host or expose a Nagios server.
