from src.awsutils import get_usernames, set_profile, get_access_key_info, get_mfa_status
from unittest import mock, TestCase
import datetime
from dateutil.tz import tzutc
from datetime import timezone


mock_boto3_client_count = 0
mock_boto3_client_responses = []
mock_list_access_keys_args = []
mock_list_access_keys_count = 0
mock_list_users_args = []
mock_list_users_count = 0
mock_list_mfa_devices_args = []
mock_list_mfa_devices_count = 0


class MockClient:
    def __init__(self, responses):
        self.responses = responses
        self.responses_count = 0

    def list_users(self, *args):
        global mock_list_users_args
        mock_list_users_args.append(args)
        response = self.responses[self.responses_count]
        self.responses_count += 1
        return response

    def list_access_keys(self, **kwargs):
        global mock_list_access_keys_args
        mock_list_access_keys_args.append(kwargs)
        response = self.responses[self.responses_count]
        self.responses_count += 1
        return response

    def list_mfa_devices(self, **kwargs):
        global mock_list_mfa_devices_args
        mock_list_mfa_devices_args.append(kwargs)
        response = self.responses[self.responses_count]
        self.responses_count += 1
        return response


def _mock_client(*args):
    global mock_boto3_client_count
    response = MockClient(mock_boto3_client_responses[mock_boto3_client_count])
    mock_boto3_client_count += 1
    return response


class TestAwsUtils(TestCase):
    def setUp(self):
        global mock_boto3_client_count
        mock_boto3_client_count = 0
        global mock_boto3_client_responses
        mock_boto3_client_responses = []
        global mock_list_users_args
        mock_list_users_args = []
        global mock_list_users_count
        mock_list_users_count = 0
        global mock_list_mfa_devices_args
        mock_list_mfa_devices_args = []
        global mock_list_mfa_devices_count
        mock_list_mfa_devices_count = 0

    @mock.patch('boto3.client', side_effect=_mock_client)
    def test_get_usernames(self, client_mock):
        global mock_boto3_client_responses
        mock_boto3_client_responses = [[{
            'Users': [{
                'UserName': 'a user',
            }, {
                'UserName': 'another user',
            }]
        }]]

        self.assertEqual(get_usernames(), ['a user', 'another user'])
        client_mock.assert_called_once_with('iam')
        self.assertEqual(mock_list_users_args, [()])

    @mock.patch('boto3.client', side_effect=_mock_client)
    def test_get_access_key_info(self, client_mock):
        global mock_boto3_client_responses
        mock_boto3_client_responses = [[
            {
                'AccessKeyMetadata': []
            },
            {
                'AccessKeyMetadata': [{
                    'CreateDate': datetime.datetime(2017, 8, 15, 6, 32, 6, tzinfo=tzutc()),
                    'UserName': 'some.user'
                }]
            }
        ]]
        today = datetime.datetime.now(timezone.utc)
        self.assertEqual(get_access_key_info(['a user', 'some.user']), {'User': ['a user', 'some.user'],
                                                                    'Access Key Age(days)': ['No Key Found.', (today - datetime.datetime(2017, 8, 15, 6, 32, 6, tzinfo=tzutc())).days]})
        client_mock.assert_called_once_with('iam')
        self.assertEqual(mock_list_access_keys_args, [{'UserName': 'a user'}, {'UserName': 'some.user'}])

    @mock.patch('boto3.client', side_effect=_mock_client)
    def test_get_mfa_status(self, client_mock):
        global mock_boto3_client_responses
        mock_boto3_client_responses = [[
            {
                'MFADevices': []
            },
            {
                'MFADevices': ['some device']
            }
        ]]

        self.assertEqual(get_mfa_status(['a user', 'some.user']), {'User': ['a user', 'some.user'],
                                                                   'MFA Status': ['NO MFA DEVICE!', 'MFA ENABLED!']})
        client_mock.assert_called_once_with('iam')
        self.assertEqual(mock_list_mfa_devices_args, [{'UserName': 'a user'}, {'UserName': 'some.user'}])

    @mock.patch('boto3.setup_default_session')
    def test_set_profile(self, setup_default_session_mock):
        set_profile('some profile')
        setup_default_session_mock.assert_called_once_with(profile_name='some profile')








