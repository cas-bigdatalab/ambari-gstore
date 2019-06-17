from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob, socket

service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

current_host_name = socket.gethostname()
# server configurations
config = Script.get_config()
master_hosts = config['clusterHostInfo']['gstore_master_hosts']
node_count=len(master_hosts)
gstore_url=config['configurations']['gstore']['gstore_url']
gstorems_url=config['configurations']['gstore']['gstorems_url']
username=config['configurations']['gstore']['username']
password=config['configurations']['gstore']['password']
node_port=config['configurations']['gstore']['node_port']
gstore_dir = config['configurations']['gstore']['home_path']
server_cnf_content=config['configurations']['gstore']['content']
collector_host= config['clusterHostInfo']['metrics_collector_hosts'][0]
