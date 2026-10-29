# This manifest is for an independently managed Linux monitoring host only.
# It does not install anything on Render.
class resume_analyzer_monitoring {
  package { 'nagios-nrpe-server':
    ensure => installed,
  }
}
