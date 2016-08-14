#!/usr/bin/env python

from optparse import OptionParser
import sys
import os
import subprocess
import re

import backends
import wrap.Config





progvers = "%prog 0.3.0"



class TerraformThis():
    def __init__(self,parameters,options,args):
        self.path = parameters['path']
        self.prog = parameters['prog']
        self.options = options
        self.args = args 
       


    def configure(self):
         subprocess_args = self.subprocess_args()
         subprocess_args.insert(0, self.prog)
         subprocess_args.insert(1, 'remote')
         subprocess_args.insert(2, 'config')
         subprocess.call(subprocess_args)

    def extras(self):
    # CREATE EXTRA ARGS THAT ARE GOING TO BE PASSED TO TERRAFORM e.g to pass 
    # any terraform native option e.g. -module or -refresh or -state etc
    # was created to add -var of -var-file
        self.extra_args = []
        for item in self.options.extra:
            new_item = item.split()
            self.extra_args.extend(new_item)
        return self.extra_args

    def run(self):
        self.configure()
        if 'plan' in self.args:
            self.plan()
        elif 'apply' in self.args:
            self.apply()
        elif 'get' in self.args:
            self.get()
        else:
            self.plan()

    def plan(self):
        subprocess_args = [self.prog, 'plan']+self.extras()
        print TextColor.YELLOW+TextColor.BOLD+"running terraform with " \
            "args "+TextColor.ENDC+str(subprocess_args)
        subprocess.call(subprocess_args)

    def apply(self):
        subprocess_args = [self.prog, 'apply']+self.extras()
        print TextColor.YELLOW+TextColor.BOLD+"running terraform with " \
            "args "+TextColor.ENDC+str(subprocess_args)
        subprocess.call(subprocess_args)

    def get(self):
        subprocess_args = [self.prog, 'get']+self.extras()
        print TextColor.YELLOW+TextColor.BOLD+"running terraform with " \
            "args "+TextColor.ENDC+str(subprocess_args)
        subprocess.call(subprocess_args)

    def s3_lock(self):
        # todo for v0.3 - create's s3  lock
        pass

    def s3_lock_release(self):
        # TODO FOR v0.3 - release s3 lock
        pass

    def s3_lock_force_release(self):
        # TODO FOR v0.3 - force release s3 lock if exists when --force-apply
        # and call s3_lock_release()
        pass

if __name__ == "__main__":
    opts = wrap
    parameters  = opts.default_params
    options = opts.options
    args = opts.args
    instance = TerraformThis(parameters,options,args)
    instance.run()


