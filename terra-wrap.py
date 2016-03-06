#!/usr/bin/python 

progvers = "%prog 0.1"

from optparse import OptionParser
import sys
import os
import subprocess
import re

terraform_bin='/home/vmindru/bin/terraform'
path='/tmp/test/'
prog=terraform_bin

default_opts = {
            'terraform_bin': terraform_bin,
            'prog': prog,
            'path': path
        }

class terraform_this():
    def __init__(self,default_opts):
        self.path=default_opts['path']
        self.prog=default_opts['prog']
        if not 'S3_REGION' in os.environ or not 'S3_BUCKET' in os.environ:
            exit('S3_REGION or S3_BUCKET  is not defined')

    def collect_opts(self):
            parser = OptionParser(version=progvers)
            parser.add_option("-k", "--key", dest = "key" , default='', help="specify S3 key where to store tfstate files")
            parser.add_option("-p", "--plan", dest="plan",  help="run terraform plan")
            parser.add_option("-a", "--apply", dest="apply", default=False , help="run terraform apply")
            parser.add_option("-c", "--clean_config", dest= "clean_config", default= False, help="remove old configs")
            (options, args) = parser.parse_args()
            self.options = options
            return options
    def get_git_dir(self):
        data = subprocess.Popen(['git','remote','show','-n','origin'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        data.wait()
        if data.returncode == 0:
            out, err = data.communicate()
            for line in out.splitlines():
                if 'Fetch' in line:
                    match = re.search('\/.*',line)
                    self.key =  match.group(0).split('.')[0].replace('/','')
        else:
            self.key = False
        return self.key

    def build_configure_args(self):
        if self.options.key == '':
            self.get_git_dir()
            if self.key == False:
                 exit("this does not look like a git folder , can not auto determine key please -k option")
            else:
               self.options.key = self.key

    def configure(self):
        if not os.path.exists(self.path+'.terraform'):
            args = self.build_configure_args()
            print "CONFIGURING TERRAFORM with opts: {},{},{}".format(self.options.key,os.environ.get('S3_REGION'),os.environ.get('S3_BUCKET'))
#            args.insert(0,self.prog)
#            args.insert(1,'plan')
#            child = subprocess.call(args)

        else:
            exit('error')
        pass
    def plan(self):
        # call this to run terraform plan
        # need to verify if .remote is configured first
        # creates lock file to prevent accident apply will use --force-apply to ingore and remove the local lock
        self.configure()
        args=sys.argv
        args.pop(0)
        args.insert(0,prog)
        child = subprocess.call(args)
    def apply(self):
        #check if lock is  present and run apply
        pass
    def force_apply(self):
        #call when --force-apply is specifyed to ignore the lock file and to skip the plan part
        pass
    def chat_lock(self):
        # todo for v0.2 - create's chat lock 
        pass
    def chat_lock_release(self):
        # TODO FOR v0.2 - release chat lockl
        pass
    def chat_lock_force_release(self):
        # TODO FOR v0.2 - force release chat lock if  exists when --force-apply and call chat_locl_release()
        pass

if __name__ == "__main__":
    instance = terraform_this(default_opts)
    opts = instance.collect_opts()
    instance.plan()
