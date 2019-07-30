import os
import base64
from time import sleep
from resource_management import *

class GStorems(Script):
    
    def install(self, env):
        import params
        env.set_params(params)
        Directory([params.gstore_dir],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd ' + params.gstore_dir + '; rm -rf gstorems-latest; wget '+params.gstorems_url+' -O gstorems.zip; unzip gstorems.zip; rm -rf gstorems.zip; ln -sf gstorems* gstorems-latest')
        
    def configure(self, env):
        import params
        env.set_params(params)
        conf_content+='{"nodeList":['
        for h in params.slave_hosts:
            conf_content+='{"nodeIp": "'+h+'","username": "'+params.username+'","password": "'+params.password+'","port": '+params.node_port+',"systemusername": "root","systempassword": "bigdata","rootpath": "'+params.gstore_dir+'/latest"}' 
        conf_content+=']}'
        File(format("{gstore_dir}/gstorems-latest/webapps/gstoremaster/Config/gStoreNodeConfig.json"), content=conf_content)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        service_packagedir = params.service_packagedir
        Execute('find '+params.service_packagedir+' -iname "*.sh" | xargs chmod +x')
        Execute(format("source /etc/profile && {gstore_dir}/gstorems-latest/bin/startup.sh"))
        Execute(format("echo \"nohup {service_packagedir}/scripts/gstore_metric_send.sh {collector_host} {current_host_name} &\"|at now"))
        Execute("ps -ef | grep -v grep | grep \"catalina.home=.*gstorems-latest\" | awk '{print $2}' >/tmp/gstorems.pid")

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(format("source /etc/profile && {gstore_dir}/gstorems-latest/bin/shutdown.sh"), ignore_failures=True)
        cmd = format("ps -ef|grep gstore_metric_send.sh |grep -v grep|cut -c 9-15|xargs kill -9 ")
        Execute(cmd, ignore_failures=True)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/tmp/gstorems.pid")

if __name__ == "__main__":
    GStorems().execute()