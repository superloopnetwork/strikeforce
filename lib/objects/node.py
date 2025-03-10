import re
import time
from netmiko import ConnectHandler
from nxapi_plumbing import Device
from slack_network_alerts import slack

class Node(object):

	def __init__(self,mgmt_ip4,hostname,device_type,username,password):

		self.mgmt_ip4 = mgmt_ip4
		self.hostname = hostname
		self.device_type = device_type
		self.username = username
		self.password = password

	def connect(self):
		self.net_connect = ConnectHandler(
								self.mgmt_ip4,
								self.hostname,
								self.username,
								self.password,
								self.password,
								device_type=self.device_type
							)

	def api_connect(self):
		self.api_connect = Device(
								api_format = "jsonrpc",
								host = self.mgmt_ip4,
								username = self.username,
								password = self.password,
								transport = "http",
								port = 80,
							)

#	def show_command(self,command):
#		output = self.net_connect.send_command(command)
#		self.net_connect.disconnect()
#
#		return output
#
#	def push_cfgs(self,commands):
#		output = self.net_connect.enable()
#		output = self.net_connect.send_config_set(commands, exit_config_mode=True)
#		save = self.net_connect.send_command('copy running-config startup-config')
	def api_config_list(self,commands):
		output = self.api_connect.config_list(commands)
		print(output)

	def api_show_interface_status(self,intf):
		slack(title = '[{}] Checking status of interface {}'.format(self.hostname,intf))
		command = 'show interface {} status'.format(intf)
		output = self.api_connect.show(command)
		status = output['TABLE_interface']['ROW_interface']['state']
		if 'connected' in status:
			result = True
			status = 'result'
		elif 'disabled' in status:
			result = False
			status = 'offline'
		elif 'notconnect' in status:
			result = False
			status = 'offline'
		elif 'xcvrAbsent' in status:
			result = False
			status = 'offline'
		slack(title = '[{}] Interface is currently {}'.format(self.hostname,status))

		return result

	def api_show_interface_crc(self,intf):
		slack(title = '[{}] Checking CRC errors on interface {}'.format(self.hostname,intf))
		command = 'show interface {}'.format(intf)
		output = self.api_connect.show(command)
		crc_error = output['TABLE_interface']['ROW_interface']['eth_crc']
		if crc_error == 0:
			result = True
			slack(title = '[{}] Interface has {} CRC errors'.format(self.hostname,crc_error))
		else:
			refresh_crc_error = output['TABLE_interface']['ROW_interface']['eth_crc']
			if refresh_crc_error > crc_error:
				result = False
				slack(title = '[{}] Interface has {} CRC errors and it\' increasing'.format(self.hostname,crc_error))
			else:
				result = True
				slack(title = '[{}] Interface has {} CRC errors'.format(self.hostname,crc_error))

		return result

	def api_show_module_status(self,module):
		slack(title = '[{}] Checking status of module {}'.format(self.hostname,module))
		command = 'show module {}'.format(module)
		output = self.api_connect.show(command)
		module_status = output['TABLE_modinfo']['ROW_modinfo']['status']
		if 'ok' in output:
			result = True
		else:
			result = False
		slack(title = '[{}] Module is currently {}.'.format(self.hostname,module_status))

		return result
		
#	def show_interface_status(self,intf):
#		slack(title = '[{}] Checking status of interface {}'.format(self.hostname,intf))
#		result = False
#		command = 'show interface {} status'.format(intf)
#		output = self.net_connect.send_command(command)
#		if 'connected' in output:
#			result = True
#			status = 'result'
#		elif 'disabled' in output:
#			result = False
#			status = 'offline'
#		elif 'notconnec' in output:
#			result = False
#			status = 'offline'
#		elif 'xcvrAbsen' in output:
#			result = False
#			status = 'offline'
#		slack(title = '[{}] Interface is currently {}'.format(self.hostname,status))
#
#		return result


#	def show_interface_crc(self,intf,CRC_RE):
#		slack(title = '[{}] Checking CRC errors on interface {}'.format(self.hostname,intf))
#		result = False
#		command = 'show interface {} | grep CRC'.format(intf)
#		output = self.net_connect.send_command(command)
#		crc_error = int(re.search(CRC_RE, output).group(1))
#		if crc_error > 0:
#			result = True
#			slack(title = '[{}] Interface has {} CRC errors'.format(self.hostname,crc_error))
#		else:
#			time.sleep(5)
#			output = self.net_connect.send_command(command)
#			refresh_crc_error = int(re.search(CRC_RE, output).group(1))
#			if refresh_crc_error > crc_error:
#				result = False
#				slack(title = '[{}] Interface has {} CRC errors'.format(self.hostname,refresh_crc_error))
#			else:
#				result = True
#				slack(title = '[{}] Interface has {} CRC errors'.format(self.hostname,refresh_crc_error))
#
#		return result 
#
#	def show_module_status(self,module):
#		slack(title = '[{}] Checking status of module {}'.format(self.hostname,module))
#		result = False
#		command = 'show module {}'.format(module)
#		output = self.net_connect.send_command(command)
#		if 'ok' in output:
#			result = True
#			status = 'result'
#		else:
#			result = False
#			status = 'offline'
#		slack(title = '[{}] Module is currently {}.'.format(self.hostname,status))
#
#		return result
#	
#	def show_module_uptime(self,module):
#		slack(title = '[{}] Checking uptime of module {}'.format(self.hostname,module))
#		uptime = 'sane'
#		command = 'show module {} | egrep -A 3 "Module {}"'.format(module,module)
#		output = self.net_connect.send_command(command)
		
		
