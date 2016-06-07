# TerraWrap

[![Code Climate](https://codeclimate.com/github/strataconsulting/terrawrap/badges/gpa.svg)](https://codeclimate.com/github/strataconsulting/terrawrap) [![Test Coverage](https://codeclimate.com/github/strataconsulting/terrawrap/badges/coverage.svg)](https://codeclimate.com/github/strataconsulting/terrawrap/coverage) [![Issue Count](https://codeclimate.com/github/strataconsulting/terrawrap/badges/issue_count.svg)](https://codeclimate.com/github/strataconsulting/terrawrap)

## Description

Terraform helper/wrapper for leveraging Terraform's [remote state S3 backend](https://www.terraform.io/docs/state/remote/s3.html).

First run will:
 * move `terraform.tfstate` into a `.terraform` directory.
 * add `terraform.tfstate.backup` file and `.terraform` directory to `.gitignore`.
 * run `terraform plan`.

## Setup

### Environment Variables
Configure the following environment variables are required:
```
export AWS_ACCESS_KEY_ID="$your_access_key"
export AWS_SECRET_ACCESS_KEY="$your_secret_key"
export S3_REGION=us-west-2
export S3_BUCKET=terraform-bucket
export TERRAWRAP_PROG='$path/to/terraform/binary'
```

### Program Soft Link (Optional)
Recommend setting up a link to the program like so:
```
ln -s terrawrap.py $HOME/bin/terrawrap
```

## Usage

```    
Usage: terrawrap [-q][-k] [plan|apply|get]

This is a terraform wrapper targeted to ensure you are always using
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
S3_REGION seems to  be set to: "us-west-2" , use this value? Y/n: Y
S3_BUCKET seems to  be set to: "strata-terraform-state-prod" , use this value? Y/n: Y
CONFIGURING TERRAFORM with opts: key: terraform-aws-vpc, region: us-west-2, bucket: terraform-state-prod
Remote state management enabled
Remote state configured and pulled.
Refreshing Terraform state prior to plan...
...
```

The impact of this run can be confirmed.

We now have a `.terraform` directory:
```
$ ls -ald .terraform
drwxr-xr-x  5 user  staff   170B Mar  8 13:38 .terraform/
```

The `terraform` directory includes local copies of `tfstate` and `tfstate.backup` files:
```
$ ls -al .terraform/terraform.tfstate*
-rw-r--r--  1 user  staff   202K Mar  8 13:38 .terraform/terraform.tfstate
-rw-r--r--  1 user  staff   201K Mar  8 13:38 .terraform/terraform.tfstate.backup
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
__Note:__ running with no argument defaults to `plan`.

## TODO

 * Add S3 locking mechanism, preventing parallel runs. 
 * Key should be created git_repo_name+git_tag+relative_path insted of simple git_repo_name+relative_path

## License

__Apache License__

## Authors
  * Veaceslav ( Slava ) Mindru (<mindruv@gmail.com>)
  * Alex Romanov (<aromanov@strataconsulting.com>)
  * Todd Michael Bushnell (<todd@strataconsulting.com>)
