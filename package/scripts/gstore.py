import os
import base64
from time import sleep
from resource_management import *

class GStoreMaster(Script):
    
    def install(self, env):      
        import params
        self.install_packages(env)
        Directory([params.gstore_dir],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd ' + params.gstore_dir + '; wget http://repo.sdc/hdp/gstore/gStore.tar.gz  -O gstore.tar.gz  ')
        Execute('cd ' + params.gstore_dir + '; tar -xvf gstore.tar.gz;rm -rf gstore.tar.gz')
        Execute('cd ' + params.gstore_dir + ';rm -rf latest; ln -s gStore* latest')          

    def configure(self, env):  
        import params
        env.set_params(params)
        server_cnf_content = InlineTemplate(params.server_cnf_content)   
        File(format("{gstore_dir}/latest/init.conf"), content=server_cnf_content)

    def start(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        service_packagedir = params.service_packagedir
        Execute('find '+params.service_packagedir+' -iname "*.sh" | xargs chmod +x')
        Execute(format("echo \"cd {gstore_dir}/latest && nohup ./bin/ghttp lubm {node_port}  2>&1 >/dev/null &\"|at now +1 min"))
        sleep(65);Execute("rm -rf /tmp/gserver.pid;pidof ./bin/ghttp | cut -d \" \" -f 1 > /tmp/gserver.pid")

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        cmd = format("ps -ef|grep ghttp |grep -v grep|cut -c 9-15|xargs kill -9 ")
        Execute(cmd, ignore_failures=True)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/tmp/gserver.pid")


if __name__ == "__main__":
    GStoreMaster().execute()
