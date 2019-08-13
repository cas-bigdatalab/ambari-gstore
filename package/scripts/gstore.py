import os
import base64
from time import sleep
from resource_management import *

class GStoreSlave(Script):
    
    def install(self, env):      
        import params
        self.install_packages(env)
        Directory([params.gstore_dir],
              mode=0755,
              cd_access='a',
              create_parents=True
        )
        Execute('cd ' + params.gstore_dir + '; rm -rf latest; wget '+params.gstore_url+' -O gstore.zip; unzip gstore.zip; rm -rf gstore.zip; ln -sf gStore* latest')
        Execute('cd ' + params.gstore_dir + '/latest; ./bin/ginit; ./bin/gbuild lubm data/lubm/lubm.nt')

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
        Execute(format("echo \"cd /data/gstore/latest && nohup ./bin/ghttp lubm {node_port}  2>&1 >/dev/null &\"|at now"))
        sleep(30)
        Execute("rm -rf /tmp/gstore-slave.pid;pidof ./bin/ghttp | cut -d \" \" -f 1 > /tmp/gstore-slave.pid")

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        cmd = format("killall ghttp")
        Execute(cmd, ignore_failures=True)

    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/tmp/gstore-slave.pid")


if __name__ == "__main__":
    GStoreSlave().execute()
