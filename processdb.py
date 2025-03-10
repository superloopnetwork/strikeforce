import yaml
from yaml import CLoader as Loader

def process_nodes():
	with open("/opt/stackstorm/kobo_code/database/nodes.yaml") as yaml_file:
		node_object = yaml.load(yaml_file,Loader=Loader)

	return node_object
