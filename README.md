# TerraWrap

## Description

Terraform helper/wrapper for leveraging Terraform's [remote state S3 backend](https://www.terraform.io/docs/state/remote/s3.html).

First run will:
 * move `terraform.tfstate` into a `.terraform` directory.
 * add `terraform.tfstate.backup` file and `.terraform` directory to `.gitignore`.

## Setup

### Environment Variables
Configure the The following environment variables are required:
```
export AWS_ACCESS_KEY_ID="$your_strata_access_key"
export AWS_SECRET_ACCESS_KEY="$your_strata_secret_key"
export S3_REGION=us-west-2
export S3_BUCKET=strata-terraform-state-prod
export TERRAWRAP_PROG='$path/to/terraform/binary'
```

### Program Soft Link (Optional)
Recommend setting up a link to the program like so:
```
ln -s terra-wrap.py $HOME/bin/terrawrap
```

## Usage

```    
Usage: terrawrap [-q][-k] [plan|apply]

This is a terraform wrapper targeted, this will make sure you are always using
S3 backned for state files

Options:
  --version          show program's version number and exit
  -h, --help         show this help message and exit
  -k KEY, --key=KEY  specify S3 key where to store tfstate files
  -q, --quiet        try to be quiet

ENV_VARS:
AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY,S3_REGION,S3_BUCKET,TERRAWRAP_PROG
```

## TODO

 * Add `[plan|apply]` to help message. __Note:__ running with no argument defaults to `plan`.
 * Add S3 locking mechanism, preventing parralel runs. 

## License

__All Rights Reserved__ (pending review)

## Authors
  * Slava Mindru (<slava@strataconsulting.com>)
