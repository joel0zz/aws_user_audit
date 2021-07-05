import boto3


def get_usernames() -> list:
    client = boto3.client('iam')
    response = client.list_users()
    aws_users = [x['UserName'] for x in response['Users']]
    return aws_users

def test():
    boto3.setup_default_session(profile_name='smart')
    iam = boto3.client("iam")
    users = get_usernames()
    for user in users:
        try:
            response = iam.get_login_profile(UserName=user)
            if response:
                print(f'{user} has console access')
        except iam.exceptions.NoSuchEntityException:
            print(f'{user} has no console access')

test()