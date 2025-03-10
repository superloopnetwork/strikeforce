import os
import sys
import re
sys.path.append('/opt/stackstorm/network_remediations')
from netmiko import ConnectHandler
from slack_network_alerts import slack

def notification(event,node):
	USER_ID_RE = r'by\s+(.+)\s+on'
	user_id = re.search(USER_ID_RE, event.error_msg).group(1)
	node.connect()
	print(event.error_msg)
	if user_id:
		slack(title = '[{}] {} EXIT configure terminal mode.'.format(node.hostname,user_id))

	return None
