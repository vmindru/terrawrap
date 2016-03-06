#!/usr/bin/python 

progvers = "%prog 0.1"

from optparse import OptionParser
import sys
import os
import subprocess

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

    def collect_opts(self):
            parser = OptionParser(version=progvers)
            parser.add_option("-r", "--region", dest = "region" ,  help="specify S3 region where to store tfstate files")
            parser.add_option("-b", "--bucket", dest = "bucket" ,  help="specify S3 bucket where to store tfstate files")
            parser.add_option("-e", "--endpoint", dest = "endpoint"  , help="specify endpoint")
            parser.add_option("-E", "--Encrypt", dest = "Encrypt" , default= True , help="Enable Encryption")
            parser.add_option("-a", "--acl", dest = "acl" , default= "private"  , help="specify acl")
            parser.add_option("-k", "--key", dest = "key" ,  help="specify S3 key where to store tfstate files")
            parser.add_option("-K", "--kms_key_id", dest = "kms_key_id" ,  help="specify kms_key_id")
            parser.add_option("-c", "--configure", dest = "configure" , default= False  , help="configure S3 remote backend")
            parser.add_option("-i", "--interactive", dest= "interactive", default= False, help="collect arguments interactive")
            parser.add_option("-C", "--clean_config", dest= "clean_config", default= False, help="remove old configs")
            (options, args) = parser.parse_args()
            self.options = options
            return options

    def build_configure_args(self):
        # Check if options.region is defined, if not propose to setup and pring ENVIRON value
        # if provide no input it will set the VAR  value equal to  ENVIRON VALUE, else set the var value 
        # equal to input
        if self.options.region != "":
            sys.stdout.write('Specify region: '+'use:'+os.getenv('S3_REGION','')+'? or specify value: ')
            region_in=sys.stdin.readline().rstrip()
            if region_in == '':
                self.options.region = os.getenv('S3_REGION','')
            else:
                self.options.region = region_in

        if self.options.bucket != "":
            sys.stdout.write('Specify bucket: '+'use:'+os.getenv('S3_BUCKET','')+'? or specify value: ')
            region_in=sys.stdin.readline().rstrip()
            if region_in == '':
                self.options.bucket = os.getenv('S3_BUCKET','')
            else:
                self.options.bucket = region_in

        if self.options.key != "":
            sys.stdout.write('Specify key: '+'use:'+os.getenv('S3_KEY','')+'? or specify value: ')
            region_in=sys.stdin.readline().rstrip()
            if region_in == '':
                self.options.key = os.getenv('S3_KEY','')
            else:
                self.options.key = region_in
        args=[self.options.region,self.options.bucket,self.options.key]
        return args    

    def configure(self):
        if not os.path.exists(self.path+'.terraform'):
            args = self.build_configure_args()
            args.insert(0,self.prog)
            args.insert(1,'plan')
            child = subprocess.call(args)
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
