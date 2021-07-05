# AWS Audit tool
## Get Access Key Age and MFA status for users.


### Setup
It's recommended to set up a virtual environment.
1. make sure your current working directory is \AWS Audit
2. python -m venv venv
3. cd venv\scripts\activate
4. cd .. back to AWS AUDIT
5. pip install -r requirements.txt

### How to run the tool
python awsaudit.py -f filename -p awsprofile(looks in .aws)

### How to run the tests.
coverage run -m unittest discover tests "*_test.py" coverage html --omit=tests/*,*/site-packages/*