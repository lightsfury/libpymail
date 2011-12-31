try:
	import syslog as _syslog
	
	syslog_codes = {key:value
				for key, value in _syslog.__dict__.items()
					if key[:4] == 'LOG_'}
	
	class LogProvider:
		def __init__(self):
			self.ResetOptions()
		
		def SetOptions(self, opts):
			if 'facility' in opts:
				try:
					self.facility = eval(opts['facility'], {"__builtins__":None}, syslog_codes)
					# Safe-eval from http://lybniz2.sourceforge.net/safeeval.html
				except:
					self.facility = opts['facility']
			
			# Pre-3.2 did not support keyword args,
			# which means we can't either
			# *angry fist shake*
			_syslog.openlog(None, 0, self.facility)
		
		def ResetOptions(self):
			self.facility = _syslog.LOG_USER
			_syslog.closelog()
			pass
		
		def __call__(self, *pargs):
			_syslog.syslog(*pargs)
	
	syslog = LogProvider()
	
except ImportError:
	class NoOpProvider:
		def SetOptions(self):
			pass
		def ResetOptions(self):
			pass
		def __call__(self):
			pass
	
	# No-op on platforms that do not support syslog
	syslog = NoOpProvider()
