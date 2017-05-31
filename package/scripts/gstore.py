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
        Execute('cd ' + params.gstore_dir + '; wget ' + params.downloadlocation + ' -O gstore.tar.gz  ')
        Execute('cd ' + params.gstore_dir + '; tar -xvf gstore.tar.gz')
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
        Execute(format("cd {gstore_dir}/latest;./bin/gserver -s;rm -rf /etc/gserver.pid;pidof ./bin/gserver | cut -d ' ' -f 1 >> /etc/gserver.pid"))

    def stop(self, env):
        import params
        env.set_params(params)
        self.configure(env)
        Execute(format("cd {gstore_dir}/latest;./bin/gserver -t"))


    def restart(self, env):
        self.stop(env)
        self.start(env)

    def status(self, env):
        check_process_status("/etc/gserver.pid")


if __name__ == "__main__":
    GStoreMaster().execute()
