from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob,socket

# server configurations
config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
server_cnf_content=config['configurations']['gstore']['content']
downloadlocation = config['configurations']['gstore']['download.location']
gstore_dir = config['configurations']['gstore']['gstore.dir']
current_host_name = socket.gethostname()
collector_host= config['clusterHostInfo']['metrics_collector_hosts'][0]
