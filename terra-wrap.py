#!/usr/bin/python 

progvers = "%prog 0.1"

from optparse import OptionParser
import sys
import os

class terraform_this():
    def __init__(self):
       pass  

    def collect_opts(self):
            parser = OptionParser(version=progvers)
            parser.add_option("-r", "--region", dest = "region" , default= "rgion"  , help="specify S3 region where to store tfstate files")
            parser.add_option("-b", "--bucket", dest = "bucket" , default= "bucket" , help="specify S3 bucket where to store tfstate files")
            parser.add_option("-e", "--endpoint", dest = "endpoint" , default= "endpoint"  , help="specify endpoint")
            parser.add_option("-E", "--Encrypt", dest = "Encrypt" , default= "Encrypt"  , help="specify endpoint")
            parser.add_option("-a", "--acl", dest = "acl" , default= "acl"  , help="specify acl")
            parser.add_option("-A", "--access_key", dest = "access_key" , default= "access_key"  , help="specify access_key")
            parser.add_option("-s", "--secret_key", dest = "secret_key" , default= "secret_key"  , help="specify secret_key")
            parser.add_option("-k", "--kms_key", dest = "kms_key" , default= "kms_key"  , help="specify kms_key")
            parser.add_option("-c", "--configure", dest = "configure" , default= "configure"  , help="specify configure")
            (options, args) = parser.parse_args()
            my_options = {
                "options": {
                        "Queue": options.queue
                            }   
            }
            return my_options
    def configure(self):
        #call this to configure terrafrom
        pass
    def plan(self):
        # call this to run terraform plan
        # need to verify if .remote is configured first
        # creates lock file to prevent accident apply will use --force-apply to ingore and remove the local lock
        pass
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
    instance = terraform_this()
    opts = instance.collect_opts()
    print opts['options']['region']
