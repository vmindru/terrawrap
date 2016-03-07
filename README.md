terraform wrapper to use S3 bucket as tfstate storage

USAGE:
    you can link this to your home e.g.
    ln -s terra-wrap.py $HOME/bin/terrawrap
    
    terrawrap [-q] [-k] [plan|apply]

        Options:
          --version          show program's version number and exit
          -h, --help         show this help message and exit
          -k KEY, --key=KEY  specify S3 key where to store tfstate files
          -q, --quite        non interactive mode, be quite.

You will have to setup following ENV variables 

export AWS_ACCESS_KEY_ID="$strata_access_key"
export AWS_SECRET_ACCESS_KEY="$strata_secret_key"
export S3_REGION=eu-west-2 
export S3_BUCKET=strata-terraform-state-prod
export TERRAWRAP_PROG='/home/vmindru/bin/terraform' # path to your terraform binnary

TODO:

    add [plan|apply] into help message no arg will run plan by default
