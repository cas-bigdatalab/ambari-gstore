import os
import base64
from time import sleep
from resource_management import *

class GStorems(Script):
    
    def install(self, env):      
        import params
        self.install_packages(env)
        Directory([params.gstore_dir],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd ' + params.gstore_dir + '; wget http://repo.sdc/hdp/gstore/gstorems.tar.gz -O gstorems.tar.gz')
        Execute('cd ' + params.gstore_dir + '; tar -xvf gstorems.tar.gz; rm -rf gstorems.tar.gz')
        Execute('cd ' + params.gstore_dir + ';rm -rf gstorems-latest; ln -sf gstorems* gstorems-latest')     

    def configure(self, env):
        import params
        env.set_params(params)
        serverms_cnf_content = InlineTemplate(params.serverms_cnf_content)   
        File(format("{gstore_dir}/gstorems-latest/webapps/gStorems/Config/gStoreInit.properties"), content=serverms_cnf_content)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        service_packagedir = params.service_packagedir
        Execute('find '+params.service_packagedir+' -iname "*.sh" | xargs chmod +x')
        Execute(format("{gstore_dir}/gstorems-latest/bin/startup.sh"))
        Execute(format("echo \"nohup {service_packagedir}/scripts/gstore_metric_send.sh {collector_host} {current_host_name} &\"|at now +1 min"))
        Execute("ps -ef | grep -v grep | grep \"catalina.home=.*gstorems-latest\" | awk '{print $2}' >/tmp/gstorems.pid")

    def stop(self, env):
        import params
        env.set_params(params)
        Execute(format("{gstore_dir}/gstorems-latest/bin/shutdown.sh"), ignore_failures=True)
        cmd = format("ps -ef|grep gstore_metric_send.sh |grep -v grep|cut -c 9-15|xargs kill -9 ")
        Execute(cmd, ignore_failures=True)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/tmp/gstorems.pid")


if __name__ == "__main__":
    GStorems().execute()