#!/usr/bin/python 

progvers = "%prog 0.1"

from optparse import OptionParser
import sys
import os
import subprocess
import re


if 'TERRAWRAP_PATH' not in os.environ:
    path=os.getcwd()
else:
    path=os.environ['TERRAWRAP_PATH']

if 'TERRAWRAP_PROG' not in os.environ:
    if os.path.exists('/usr/bin/terraform'):
        path='/usr/bin/terraform'
    else:
        exit('please define TERRAWRAP_PROG env var , this should be full path to your terraform binary')
else:
    prog=os.environ.get('TERRAWRAP_PROG')

default_opts = {
            'prog': prog,
            'path': path,
        }

class terraform_this():
    def __init__(self,default_opts):
        self.path=default_opts['path']
        self.prog=default_opts['prog']
        if not 'S3_REGION' in os.environ or not 'S3_BUCKET' in os.environ:
            exit('S3_REGION or S3_BUCKET one or both ENV vars are not defined')
        self.collect_opts()

    def collect_opts(self):
            parser = OptionParser(version=progvers)
            parser.description='This is a terraform wrapper targeted, this will make sure you are always using S3 backned for state files'
            parser.add_option("-k", "--key", dest = "key" , default='', help="specify S3 key where to store tfstate files")
            parser.add_option("-q", "--quite", dest='quite' , action='store_true', default = False, help="try to be quite")
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
                if 'S3_KEY' in os.environ and self.options.quite == False:
                    answer = ''
                    while answer not in ['Yes','yes','No','no']:
                        sys.stdout.write("S3_KEY seems to  be set to: \"%s\" , use this value? Yes|No: " % os.environ.get('S3_KEY'))
                        answer = sys.stdin.readline().rstrip()
                    if answer in ['Yes','yes']:
                        self.options.key = os.environ.get('S3_KEY')
                    elif answer in ['No', 'no']:
                        exit("this does not look like a git folder, i can not auto determine key , and you forbid me to use the S3_KEY env, please use -k|-K option")
                elif 'S3_KEY' in os.environ and self.options.quite == True:
                    self.options.key = os.environ.get('S3_KEY')
                else:
                    exit("this does not look like a git folder , can not auto determine key please -k option")
            else:
               self.options.key = self.key

        if 'S3_REGION' in os.environ and self.options.quite == False:
            answer = ''
            while answer not in ['Yes','yes','No','no']:
                sys.stdout.write("S3_REGION seems to  be set to: \"%s\" , use this value? Yes|No: " % os.environ.get('S3_REGION'))
                answer = sys.stdin.readline().rstrip()
            if answer in ['Yes','yes']:
                self.options.region = os.environ.get('S3_REGION')
            elif answer in ['No', 'no']:
                exit("i can not auto determine bucket , pleas correct S3_BUCKET env var")
        elif 'S3_REGION' in os.environ and self.options.quite == True:
            self.options.region = os.environ.get('S3_REGION')
        else:
            exit("this does not look like a git folder , can not auto determine region please -k option")

        if 'S3_BUCKET' in os.environ and self.options.quite == False:
            answer = ''
            while answer not in ['Yes','yes','No','no']:
                sys.stdout.write("S3_BUCKET seems to  be set to: \"%s\" , use this value? Yes|No: " % os.environ.get('S3_BUCKET'))
                answer = sys.stdin.readline().rstrip()
            if answer in ['Yes','yes']:
                self.options.bucket = os.environ.get('S3_BUCKET')
            elif answer in ['No', 'no']:
                exit("i can not auto determine bucket , pleas correct S3_BUCKET env var")
        elif 'S3_BUCKET' in os.environ and self.options.quite == True:
            self.options.bucket = os.environ.get('S3_BUCKET')
        else:
            exit("this does not look like a git folder , can not auto determine bucket please -k option")

    def configure(self):
        if not os.path.exists(self.path+'.terraform'):
            self.build_configure_args()
            print "CONFIGURING TERRAFORM with opts: key: {}, region: {}, bucket: {}".format(self.options.key,
                                                                                            os.environ.get('S3_REGION'),
                                                                                            os.environ.get('S3_BUCKET'))
            args_plan = ["-backend=s3", 
                        "-backend-config=bucket="+self.options.bucket,
                        "-backend-config=region="+self.options.region,
                        "-backend-config=key="+self.options.key,
                    ]
            args_plan.insert(0,self.prog)
            args_plan.insert(1,'remote')
            args_plan.insert(2,'config')
            child = subprocess.call(args_plan)

        pass

    def run(self):
        # call this to run terraform plan
        # need to verify if .remote is configured first
        # creates lock file to prevent accident apply will use --force-apply to ingore and remove the local lock
        self.configure()
        self.args=sys.argv
        if 'plan' in self.args:
            self.plan()
        elif 'apply' in self.args:
            self.apply()
        else:
            self.plan()

    def plan(self):
        args_plan = [self.prog,'plan']
        child = subprocess.call(args_plan)

    def apply(self):
        args_plan = [self.prog,'apply']
        child = subprocess.call(args_plan)

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
    instance.run()
