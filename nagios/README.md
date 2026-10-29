# Nagios HTTP check starter

Copy `commands.cfg` to the Nagios server's command configuration and `services.cfg` to the configuration directory for the monitored host/service. Replace `YOUR-SERVICE.onrender.com` with the public Render hostname, then validate/reload Nagios using the commands for your distribution. This probes the public URL only; it does not install or run Nagios inside Render. The Nagios server must have outbound HTTPS access.
