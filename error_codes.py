import importlib.util

def error_codes(ERROR_CODE,action):
	"""
		:param ERROR_CODES_TO_REMEDIATIONS.key: Match syslog error code.
		:type ERROR_CODES_TO_REMEDIATIONS.key: str

		:param ERROR_CODES_TO_REMEDIATIONS.value: Name of module placed in /opt/stackstorm/kbar/lib/modules/
		:type ERROR_CODES_TO_REMEDIATIONS.value: str
	"""

	ERROR_CODES_TO_REMEDIATIONS = {
		'ETHPORT-5-IF_DOWN_ADMIN_DOWN': 'ethport_5_if_down_admin_down',
#		'VSHD-5-VSHD_SYSLOG_CONFIG_I': 'vshd-5-vshd_syslog_config_i',
		}
	if ERROR_CODE in ERROR_CODES_TO_REMEDIATIONS:
		error_code_module = ERROR_CODES_TO_REMEDIATIONS[ERROR_CODE]
		spec = importlib.util.spec_from_file_location('{}'.format(ERROR_CODE), '/opt/stackstorm/kbar/lib/modules/{}.py'.format(error_code_module))
		module = importlib.util.module_from_spec(spec)
		spec.loader.exec_module(module)

	return module
