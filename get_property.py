def get_device_type(mgmt_ip4, node_object):

	for node in node_object:
		if mgmt_ip4 == node['mgmt_ip4']:
			index = node_object.index(node)
			break
		else:
			pass
	device_type = node_object[index]['hardware_vendor'] + '_' + node_object[index]['opersys']

	return device_type
