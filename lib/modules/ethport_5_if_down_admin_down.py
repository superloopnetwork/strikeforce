import os
import sys
import re
sys.path.append('/opt/stackstorm/kbar')
from slack_network_alerts import slack

def notification(event,node):
	CRC_RE = r'(\d+)\s+CRC'
	INTERFACE_RE = r'.+\s(\w+\d+\/\d+)'
	MODULE_RE = r'(\d+)\/\d+'
	intf = re.search(INTERFACE_RE, event.error_msg).group(1)
	module = re.search(MODULE_RE, intf).group(1)
	slack(title = '[{}] Log event matched for remediation %{}'.format(node.hostname,event.error_code))
#	node.connect()
	node.api_connect()
	status = node.api_show_interface_status(intf)
	crc_errors = node.api_show_interface_crc(intf)
	module_status = node.api_show_module_status(module)
	methods = [
		node.api_show_interface_status(intf),
		node.api_show_interface_crc(intf),
		node.api_show_module_status(module),
		]
#		node.api_show_interface_status(intf)
#		node.show_interface_status(intf),
#		node.show_interface_crc(intf,CRC_RE),
#		node.show_module_status(module),
#		]
	for method in methods:
		"""
			If it returns False, break out of for loop.
		"""
		if not method:
			slack(title = '[{}] Remediating...'.format(node.hostname))
			remediation(node,intf)
			slack(title = '[{}] Interface is brought back online. Taking no further actions'.format(node.hostname,intf))
			break
			
	else:
		slack(title = 'Module uptime appears sane. Taking no further actions')

	return None

def remediation(node,intf):

	remediation = [
		'interface {}'.format(intf),
		'no shutdown'
	]
	node.api_config_list(remediation)

	return None
