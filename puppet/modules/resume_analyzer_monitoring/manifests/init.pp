class resume_analyzer_monitoring {
  package { 'nagios-plugins-basic':
    ensure => installed,
  }

  file { '/etc/nagios4/conf.d/resume-analyzer.cfg':
    ensure  => file,
    owner   => 'root',
    group   => 'root',
    mode    => '0644',
    content => template('resume_analyzer_monitoring/resume-analyzer.cfg.erb'),
    require => Package['nagios-plugins-basic'],
  }

  service { 'nagios4':
    ensure  => running,
    enable  => true,
    require => File['/etc/nagios4/conf.d/resume-analyzer.cfg'],
  }

  service { 'apache2':
    ensure  => running,
    enable  => true,
    require => Service['nagios4'],
  }
}
