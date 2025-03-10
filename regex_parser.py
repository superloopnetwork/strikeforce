import re
from lib.objects.event import Event

def regex_parser(device_type,syslog_line):

	if device_type == 'cisco_nxos':
		event = regex_parser_cisco_nxos(syslog_line)
	else:
		print('[x] No regex has been configured for device type \'{}\''.format(device_type))

	return event

def regex_parser_cisco_nxos(syslog_line):

	COLUMN_DELIMITER_RE = r'(\s+)'
	DEVICE_IP_RE = r'(\d+\.\d+\.\d+\.\d+)'
	DATESTAMP_RE = r'(\d+\s+\w+\s+\d+)'
	ERROR_CODE_RE = r'%(\S+):'
	ERROR_MESSAGE_RE = r'(.*)'
	HOSTNAME_RE = r'(\w+\-\w+\-\d+):'
	INDEX_RE = r'(<\d+>)'
	TIMESTAMP_RE = r'(\d+:\d+:\d+.\d+)'
	TIMEZONE_RE = r'(\w+):'

	SYSLOG_RE = INDEX_RE + HOSTNAME_RE + COLUMN_DELIMITER_RE + DATESTAMP_RE + COLUMN_DELIMITER_RE + TIMESTAMP_RE + COLUMN_DELIMITER_RE + TIMEZONE_RE + COLUMN_DELIMITER_RE + ERROR_CODE_RE + COLUMN_DELIMITER_RE + ERROR_MESSAGE_RE
	match_RE = re.match(SYSLOG_RE, syslog_line)

	if match_RE:
		hostname = match_RE.group(2)
		dstamp = match_RE.group(4)
		tstamp = match_RE.group(6)
		timezone = match_RE.group(8)
		error_code = match_RE.group(10)
		error_msg = match_RE.group(12)

	event = Event(dstamp,tstamp,hostname,timezone,error_code,error_msg)

	return event 
