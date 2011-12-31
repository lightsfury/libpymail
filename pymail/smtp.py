from configparser import ConfigParser
from smtplib import SMTP, SMTP_SSL
from .syslog import syslog

exception_messages = {
	"DOMAIN_MISSING": "Cannot find specified configuration domain: `%s'.",
	"DOMAIN_MISSING_HOST": "Specified configuration domain (`%s') missing required `host' field.",
	"DOMAIN_INVALID_AUTH": "Specified configuration domain (`%s') has an empty authorization section (`%s'). Remove the authorization section or add `user' and `pass' entries to the authorization section."
}

class PyMail:
	def __init__(self, **kargs):
		LoadConfig(**kargs)
	
	def OpenConnection(self, domain = None, **kargs):
		info = GetDomainInformation(domain = domain)
		
		try:
			if info.ssl:
				smtp = SMTP_SSL
			else:
				smtp = SMTP
			
			connection = smtp(host = info.host, port = info.port)
			
			if info.auth:
				connection.login(user = info.auth_user, password = info.auth_pass)
		except:
			syslog(exception_messages["SMTP_EXCEPTION"])
			raise
	
	def LoadConfig(self, config_path = None, default_domain = None, **kargs):
		if not config_path:
			config_path = '/etc/pymail.conf'
		ini = ConfigParser()
		ini.read(config_path)
		
		if not default_domain and ini.has_option('global', 'default_domain'):
			default_domain = ini.get('global', 'default_domain')
		
		if ini.has_option('logging'):
			syslog.SetupOptions(ini['logging'])
		
		self.config = ini
		self.default_domain = default_domain
		pass
	
	def GetDomainInformation(self, domain = None):
		if not domain:
			domain = self.default_domain
		domain_auth = domain + ':auth'
		ret = object()
		
		if not ini.has_section(domain):
			raise ValueError(exception_messages["DOMAIN_MISSING"] % (domain))
		
		if ini.has_option(domain, 'host'):
			ret.host = ini.get(domain, 'host')
		else:
			raise ValueError(exception_messages["DOMAIN_MISSING_HOST"] % (domain))
		
		if ini.has_option(domain, 'ssl'):
			ret.ssl = ini.getboolean(domain, 'ssl')
		else
			ret.ssl = False
		
		if ini.has_option(domain, 'port'):
			ret.port = ini.getint(domain, 'port')
		else:
			if ret.ssl:
				ret.port = 465
			else:
				ret.port = 25
		
		if ini.has_section(domain_auth):
			ret.auth = True
			
			if ini.has_option(domain_auth, 'user') and ini.has_option(domain_auth, 'pass'):
				ret.auth_user = ini.get(domain_auth, 'user')
				ret.auth_pass = ini.get(domain_auth, 'pass')
			else:
				raise ValueError(exception_messages["DOMAIN_INVALID_AUTH"] % (domain, domain_auth))
		else:
			ret.auth = False
		
		return ret
		pass

"""
class PyMail:
	def __init__(self, *kargs):
		self.SetupOptions(**kargs)
	
	def OpenConnection(self, **kargs):
		if 'config_path' in kargs:
			self.config_path = kargs['config_path']
		
		self.LoadConfig(**kargs)
		
		if 'host' in self.config_values: # Only required data member
			# Open the SMTP connection here
			pass
	
	def Close(self):
		self.config_path = '/etc/libpymail/pymail.ini'
		self.config_values = {}
		self.default_config_domain = ''
		#self.log_facility = "LOG_MAIL"
		
	def LoadConfig(self, **kargs):
		ini = ConfigParser()
		ini.read(self.config_path)
		
		# Parse ini file
		if ini.has_section('global') and ini.has_option('global', 'default_domain'):
			self.default_config_domain = ini.get('global', 'default_domain')
			
		if 'domain' in kargs:
			self.default_config_domain = kargs['domain']
		
		# Load domain information
		if ini.has_section(self.default_config_domain):
			if ini.has_option(self.default_config_domain, 'host'):
				self.config_values['host'] = ini.get(self.default_config_domain, 'host')
			else:
				raise ValueError("Specified domain (`%s') configuration missing required `host' option." %s (self.default_config_domain))
			
			if ini.has_option(self.default_config_domain, 'ssl'):
				self.config_values['ssl'] = ini.getboolean(self.default_config_domain, 'ssl')
			
			if ini.has_option(self.default_config_domain, 'port'):
				self.config_values['port'] = ini.getint(self.default_config_domain, 'port')
			else:
				if self.config_values['ssl']:
					self.config_values['port'] = 465
				else:
					self.config_values['port'] = 25
		else:
			raise ValueError("Specified configuration domain `%s' does not exist in the INI file." % (self.default_config_domain))
		
		## Load authentication details
		if ini.has_section(self.default_config_domain + ':auth'):
			if ini.has_option(self.default_config_domain + ':auth', 'user'):
				self.config_values['auth_user'] = ini.get(self.default_config_domain + ':auth', 'user')
			else:
				raise ValueError("Empty authentication section present for specified configuration domain (`%s')." % (self.default_config_domain))
			
			if ini.has_option(self.default_config_domain + ':auth', 'pass'):
				self.config_values['auth_pass'] = ini.get(self.default_config_domain + ':auth', 'pass')
			else:
				# Should an exception be thrown here?
				pass
		
		# Setup syslog
		if ini.has_section('logging'):
			syslog.SetupOptions(ini['logging'])
"""