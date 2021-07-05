import boto3
from datetime import datetime, timezone
from pprint import pprint


def get_usernames() -> list:
    client = boto3.client('iam')
    response = client.list_users()
    aws_users = [x['UserName'] for x in response['Users']]
    return aws_users


def get_access_key_info(users: list) -> dict:
    client = boto3.client('iam')
    response = [client.list_access_keys(UserName=user) for user in users]
    access_key_info = {'User': [], 'Access Key Age(days)': []}
    today = datetime.now(timezone.utc)
    for index, item in enumerate(response):
        if not item['AccessKeyMetadata']:
            access_key_info['Access Key Age(days)'].append('No Key Found.')
            access_key_info['User'].append(users[index])
        else:
            for key_meta in item['AccessKeyMetadata']:
                access_key_info['Access Key Age(days)'].append((today - key_meta['CreateDate']).days)
                access_key_info['User'].append(key_meta['UserName'])
    return access_key_info


def get_mfa_status(users: list) -> dict:
    client = boto3.client('iam')
    response = [client.list_mfa_devices(UserName=user) for user in users]
    mfa_status = {'User': [], 'MFA Status': [], 'Console Access': []}
    for index, item in enumerate(response):
        mfa_status['User'].append(users[index])
        if not item['MFADevices']:
            mfa_status['MFA Status'].append('NO MFA DEVICE!')
        else:
            mfa_status['MFA Status'].append('MFA ENABLED!')
    for user in users:
        try:
            response = client.get_login_profile(UserName=user)
            if response:
                mfa_status['Console Access'].append('YES')
        except client.exceptions.NoSuchEntityException:
            mfa_status['Console Access'].append('NO')
    return mfa_status


def set_profile(name: str):
    boto3.setup_default_session(profile_name=name)

