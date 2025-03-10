import os
import sys
import re
sys.path.append('/opt/stackstorm/network_remediations')
from error_codes import error_codes
from get_property import get_device_type
from processdb import process_nodes 
from regex_parser import regex_parser
from lib.objects.node import Node

action = sys.argv[1]

def system_handler(action):
	node_object = process_nodes()
	mgmt_ip4 = sys.argv[2]
	syslog_line = sys.argv[3]
	device_type = get_device_type(mgmt_ip4,node_object)
	username = os.environ.get('NETWORK_USERNAME')
	password = os.environ.get('NETWORK_PASSWORD')

	event = regex_parser(device_type,syslog_line)
	
	node = Node(mgmt_ip4,event.hostname,device_type,username,password)

	module = error_codes(event.error_code,action)
	if action == 'notification':
		module.notification(event,node)
	elif action == 'remediation':
		module.remediation(event,node)

	return None

if __name__ == '__main__':
	system_handler(action)
