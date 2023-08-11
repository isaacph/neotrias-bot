# neotrias-bot
A discord bot for managing a Minecraft server

## Setting up the discord bot
Refer to a bunch of tutorials. Will link these here later

## Setting up the AWS Lambda function
1. Make this into a virtual environment

Source: https://medium.com/@jtpaasch/the-right-way-to-use-virtual-environments-1bc255a0cba7

Make sure Python is version 3.10

```
> python3.10 --version
Python 3.10.12
```

Make virtual environment
```
> pwd
SOME_PATH/neotrias-bot
> python3.10 -m venv env
> source env/bin/activate
> pip install -r requirements.txt
Requirement already satisfied: boto3==1.28.25 in ./env/lib/python3.10/site-packages (from -r requirements.txt (line 1)) (1.28.25)
etc
> deactivate
```

2. Zip for use with Lambda

Source: https://docs.aws.amazon.com/lambda/latest/dg/python-package.html

```
> cd env/lib/python3.10/site-packages
> zip -r ../../../../function.zip .
adding: cffi/ (stored 0%)
adding: cffi/error.py (deflated 61%)
adding: cffi/__pycache__/ (stored 0%)
adding: cffi/__pycache__/backend_ctypes.cpython-310.pyc (deflated 61%)
etc
> cd ../../../..
> zip function.zip lambda_function.py public_key.py
adding: lambda_function.py (deflated 72%)
adding: public_key.py (deflated 8%)
```

3. Upload to the Lambda function
