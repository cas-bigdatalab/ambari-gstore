from resource_management import *
from resource_management.libraries.script.script import Script
import sys, os, glob,socket

# server configurations
config = Script.get_config()
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]
gstore_dir = "/data/gstore"
server_cnf_content=config['configurations']['gstore']['content']
serverms_cnf_content=config['configurations']['gstore']['ms.content']
current_host_name = socket.gethostname()
node_index=serverms_cnf_content.split("="+current_host_name)[0][-1]
node_port=serverms_cnf_content.split("port"+node_index+"=")[1].split()[0]
collector_host= config['clusterHostInfo']['metrics_collector_hosts'][0]