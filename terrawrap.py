#!/usr/bin/env python

from optparse import OptionParser
import sys
import os
import subprocess
import re

progvers = "%prog 0.2.1"


class tcol:
    YELLOW = '\033[33m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class GetOpts():
    def __init__(self):
            self.collect_opts()
            self.init_default_params()
    
    def init_default_params(self):
            if 'TERRAWRAP_PATH' not in os.environ:
                path = os.getcwd()
            else:
                path = os.environ['TERRAWRAP_PATH']
    
            if 'TERRAWRAP_PROG' not in os.environ:
                if os.path.exists('/usr/bin/terraform'):
                    prog = '/usr/bin/terraform'
                else:
                    exit('TERRAWRAP_PROG env var not defined, this should be full '
                         'path to your terraform binary')
            else:
                if os.path.exists(os.environ.get('TERRAWRAP_PROG')):
                    prog = os.environ.get('TERRAWRAP_PROG')
                else:
                    exit('could not find TERRAWRAP_PROG binnary ,please define '
                         'TERRAWRAP_PROG env var, this should be full path to your'
                         ' terraform binary')
    
            default_params = {"prog": prog,
                            "path": path,
                            }
    
    
            self.default_params = default_params
    
    def collect_opts(self):
            parser = OptionParser(version=progvers,
                                  usage=("usage: %prog [-q][-k]"
                                         "[plan|apply|get]"),
                                  )
            parser.description = ('This is a terraform wrapper targeted, this '
                                  'will make sure you are always using state'
                                  'backned like s3, swift or http for state files')
            parser.add_option("-k",
                              "--key",
                              dest="key",
                              default='',
                              help="specify S3 key where to \
                                    store tfstate files")
            parser.add_option("-q",
                              "--quiet",
                              dest='quiet',
                              action='store_true',
                              default=False, help="reduce verbosity to quiet")
            parser.add_option("-a",
                              "--action",
                              dest='action',
                              default='plan',
                              help="specify action plan|apply|get")
            parser.add_option("-e",
                              "--extra",
                              dest='extra',
                              action='append',
                              default=[],
                              help="specify native terraform options e.g. too pass\
                                    -var foo=bar specify terrawrap --extra '-var\
                                    foo=bar'")
            parser.add_option("-b",
                              "--backend",
                              dest='backend',
                              default='s3',
                              help="specify our remote state backend, you can get\
                                    more details on terraform documentation page\
                                    https://www.terraform.io/docs/state/remote")
                                    
            
            (options, args) = parser.parse_args()
            self.options = options
            self.args = args 



class TerraformThis():
    def __init__(self,parameters,options,args):
        self.path = parameters['path']
        self.prog = parameters['prog']
        self.options = options
        self.args = args 
       

    def key_from_git(self):
    # try to auto figure out the key , if no GIT origin is present we will ask to
    # inpute -k option 
    #TODO: change this to simple check of the file insted of calling the GIT command
        data = subprocess.Popen(['git', 'remote', 'show', '-n', 'origin'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        data.wait()
        if data.returncode == 0:
            out, err = data.communicate()
            for line in out.splitlines():
                if 'Fetch' in line:
                    match = re.search('\/.*', line)
                    if match is not None:
                        key = match.group(0).split('.')[0]
                        key.replace('/', '')

                    else:
                        exit('Can not figure out the repo name base on your '
                             'origin, please use -k key to specify the key')
        else:
            exit('Your git does not seem to have a remote origin. Please set '
                 'it or use -k key to specify the key.')

        # let's find out the relative path to the .git base this will be used
        # to compound the S3_KEY
        data = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        data.wait()
        if data.returncode == 0:
            self.top_level_path, err = data.communicate()
            self.top_level_path = self.top_level_path.rstrip()
        else:
            exit('Can not determine the relative path, please create an issue'
                 ' at https://github.com/strataconsulting/terrawrap/ .')

        # CONVERT STRING TO ARRAY AND SUBSTRACT THE RELATIVE PATH
        s0 = self.path.split('/')
        s1 = self.top_level_path.split('/')
        for item in s1:
            s0.remove(item)
        self.relative_path = "/".join(s0)
        return key

    def s3_build_configure_args():
        # DO S3 PREPAREATIONS as per https://www.terraform.io/docs/state/remote/s3.html

        valid_yes = ['Yes', 'yes', 'Y', 'y'] 
        valid_no = ['No', 'no', 'N', 'n']
        valid_answers = valid_yes + valid_no

             if 'S3_KEY' in os.environ and self.options.quiet is False:
                 answer = 'UNDEF'
                 while answer not in valid_answers:
                     sys.stdout.write("S3_KEY seems to  be set to: \"%s\",\
                                       use this value? Y/n: "
                                      % os.environ.get('S3_KEY')
                                      )
                     answer = sys.stdin.readline().rstrip()
                 if answer in valid_yes: 
                     self.options.key = os.environ.get('S3_KEY')
                 elif answer in valid_no:  
                     exit("This does not look like a git folder, i can not"
                          " auto determine key, please use -k option")
                 if answer in ['']:
                     self.options.key = os.environ.get('S3_KEY')

             elif 'S3_KEY' in os.environ and self.options.quiet is True:
                 self.options.key = os.environ.get('S3_KEY')
             else:
                 exit("this does not look like a git folder, can not auto"
                      " determine key please -k option")
         if 'S3_REGION' in os.environ and self.options.quiet is False:
            answer = 'UNDEF'
            while answer not in valid_answers:
                sys.stdout.write("S3_REGION seems to be set to: \"%s\",use"
                                 "this value? Y/n: "
                                 % os.environ.get('S3_REGION')
                                 )
                answer = sys.stdin.readline().rstrip()

            if answer in valid_yes:
                self.options.region = os.environ.get('S3_REGION')
            elif answer in valid_no:
                exit("I can not auto determine bucket,"
                     "please correct S3_BUCKET env var")
            if answer in ['']:
                self.options.region = os.environ.get('S3_REGION')

        elif 'S3_REGION' in os.environ and self.options.quiet is True:
            self.options.region = os.environ.get('S3_REGION')
        else:
            exit("This does not look like a git folder,"
                 "cannot auto determine region please use -k option")

               if 'S3_BUCKET' in os.environ and self.options.quiet is False:
            answer = 'UNDEF'
            while answer not in valid_answers:
                sys.stdout.write("S3_BUCKET seems to be set to: \"%s\", use"
                                 "this value? Y/n: "
                                 % os.environ.get('S3_BUCKET'))
                answer = sys.stdin.readline().rstrip()
            if answer in valid_yes:
                self.options.bucket = os.environ.get('S3_BUCKET')
            elif answer in valid_no:
                exit("I can not auto determine bucket, please correct "
                     "S3_BUCKET env var")
            if answer in ['']:
                self.options.bucket = os.environ.get('S3_BUCKET')

        elif 'S3_BUCKET' in os.environ and self.options.quiet is True:
            self.options.bucket = os.environ.get('S3_BUCKET')



    def build_configure_args(self):
        """ builds terraform remote config args, returns [] with args"""
        # DEFAULT THE RELATIVE PATH TO '' IN CASE YOU ARE RUNNING THIS FOR NON
        # GIT with -K option
        self.relative_path = ''
        key = self.key_from_git() 
        if self.options.key == '':
        # CHECK IF self.options.key has a value, if it's kalled with -k param.
        # if not check if we are running on GIT 

    def subprocess_args(self):
        """ BEFORE EVERY RUN , TERRAFORM WILL MAKE SURE OUR STATE BACKEND IS CONFIGURED
             IT WILL PREPARE THE ARGS AND CALL terraform remote config WITH COMPUTED ARGS"""
        subprocess_args = []
        if self.options.backend == 's3':
            if not os.path.exists(self.path+'.terraform'):
                self.build_configure_args()
                print tcol.YELLOW+tcol.BOLD+"updating remote config"+tcol.ENDC
                print ("CONFIGURING TERRAFORM with opts: key: {}, region: {}, buc"
                       "ket: {}").format(self.options.key,
                                         os.environ.get('S3_REGION'),
                                         os.environ.get('S3_BUCKET')
                                         )
                subprocess_args = ["-backend=s3",
                             "-backend-config=bucket="+self.options.bucket,
                             "-backend-config=region="+self.options.region,
                             "-backend-config=key="+self.options.key+"/" +
                             self.relative_path +
                             "/terraform.tfstate",
                             ]
        elif self.options.backend == 'swift':
            if not os.path.exists(self.path+'.terraform'):
                self.build_configure_args()
                print tcol.YELLOW+tcol.BOLD+"updating remote config"+tcol.ENDC
                print ("CONFIGURING TERRAFORM with opts: key: {}, region: {}, buc"
                       "ket: {}").format(self.options.key,
                                         os.environ.get('S3_REGION'),
                                         os.environ.get('S3_BUCKET')
                                         )
                subprocess_args = ["-backend=s3",
                             "-backend-config=bucket="+self.options.bucket,
                             "-backend-config=region="+self.options.region,
                             "-backend-config=key="+self.options.key+"/" +
                             self.relative_path +
                             "/terraform.tfstate",
                             ]
        return subprocess_args   

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
        print tcol.YELLOW+tcol.BOLD+"running terraform with " \
            "args "+tcol.ENDC+str(subprocess_args)
        subprocess.call(subprocess_args)

    def apply(self):
        subprocess_args = [self.prog, 'apply']+self.extras()
        print tcol.YELLOW+tcol.BOLD+"running terraform with " \
            "args "+tcol.ENDC+str(subprocess_args)
        subprocess.call(subprocess_args)

    def get(self):
        subprocess_args = [self.prog, 'get']+self.extras()
        print tcol.YELLOW+tcol.BOLD+"running terraform with " \
            "args "+tcol.ENDC+str(subprocess_args)
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
    opts = getOpts()
    parameters  = opts.default_params
    options = opts.options
    args = opts.args
    instance = TerraformThis(parameters,options,args)
    instance.run()


