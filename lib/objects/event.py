class Event(object):

	def __init__(self,dstamp,tstamp,hostname,timezone,error_code,error_msg):

		self.dstamp = dstamp
		self.tstamp = tstamp
		self.hostname = hostname
		self.timezone = timezone
		self.error_code = error_code 
		self.error_msg = error_msg
