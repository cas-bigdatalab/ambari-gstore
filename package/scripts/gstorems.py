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
        Execute('cd ' + params.gstore_dir + '; wget '+params.gstorems_url+' -O gstorems.tar.gz')
        Execute('cd ' + params.gstore_dir + '; tar -xvf gstorems.tar.gz; rm -rf gstorems.tar.gz')
        Execute('cd ' + params.gstore_dir + ';rm -rf gstorems-latest; ln -sf gstorems* gstorems-latest')     

    def configure(self, env):
        import params
        env.set_params(params)
        conf_content="nodecount={}".format(params.node_count)
        for index in range(params.node_count):
            conf_content+='\n\n#NODE{index} INFO \nport{index}={port}'.format(index=index+1,port=params.node_port)
            conf_content+='\nip{}={}'.format(index+1,params.master_hosts[index])
            conf_content+='\nusername{}={}'.format(index+1,params.username)
            conf_content+='\nrootpath{}={}/latest'.format(index+1,params.gstore_dir)
            conf_content+='\nsystemusername{}=root'.format(index+1)
            conf_content+='\nsystempassword{}=bigdata'.format(index+1)

        File(format("{gstore_dir}/gstorems-latest/webapps/gStorems/Config/gStoreInit.properties"), content=conf_content)

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