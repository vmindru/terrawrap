# TerraWrap

## Description

Terraform helper/wrapper for leveraging Terraform's [remote state S3 backend](https://www.terraform.io/docs/state/remote/s3.html).

First run will:
 * move `terraform.tfstate` into a `.terraform` directory.
 * add `terraform.tfstate.backup` file and `.terraform` directory to `.gitignore`.
 * run `terraform plan`.

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

Below is a sample first run from inside a Terraform project directory

```
$ terrawrap
S3_REGION seems to  be set to: "us-west-2" , use this value? Y/N: Y
S3_BUCKET seems to  be set to: "strata-terraform-state-prod" , use this value? Y/N: Y
CONFIGURING TERRAFORM with opts: key: terraform-aws-vpc, region: us-west-2, bucket: strata-terraform-state-prod
Remote state management enabled
Remote state configured and pulled.
Refreshing Terraform state prior to plan...
...
```

The impact of this run can be confirmed.

We now have a `.terraform` directory:
```
$ ls -ald .terraform
drwxr-xr-x  5 tmichael  staff   170B Mar  8 13:38 .terraform/
```

The `terraform` directory includes local copies of `tfstate` and `tfstate.backup` files:
```
$ ls -al .terraform/terraform.tfstate*
-rw-r--r--  1 tmichael  staff   202K Mar  8 13:38 .terraform/terraform.tfstate
-rw-r--r--  1 tmichael  staff   201K Mar  8 13:38 .terraform/terraform.tfstate.backup
```

The `terraform.tfstate` file has been `git rm` removed:
```
$ git status terraform.tfstate
On branch master
Your branch is up-to-date with 'origin/master'.
Changes not staged for commit:
  (use "git add/rm <file>..." to update what will be committed)
  (use "git checkout -- <file>..." to discard changes in working directory)

	deleted:    terraform.tfstate
```

## TODO

 * Add statefile locking mechanism
 * Add `[plan|apply]` to help message. __Note:__ running with no argument defaults to `plan`.
 * Add S3 locking mechanism, preventing parralel runs. 

## License

__All Rights Reserved__ (pending review)

## Authors
  * Slava Mindru (<slava@strataconsulting.com>)
