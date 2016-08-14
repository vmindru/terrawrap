
class BackendConfigs():
    def __init__(self):
        pass

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
