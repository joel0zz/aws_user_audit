from awsaudit import main
from unittest import mock, TestCase
from unittest.mock import call


class MockArgs:
    profile = 'some profile'
    filename = 'some filename'


def _mock_get_access_key_info(*args):
    return 'some access key info'


def _mock_get_mfa_status(*args):
    return 'some mfa info'


def _mock_get_usernames():
    return 'some usernames'


def _mock_parse_args(*args):
    return MockArgs()


class TestAWSAudit(TestCase):
    @mock.patch('awsaudit.get_mfa_status', side_effect=_mock_get_mfa_status)
    @mock.patch('awsaudit.get_access_key_info', side_effect=_mock_get_access_key_info)
    @mock.patch('awsaudit.export_to_csv')
    @mock.patch('awsaudit.set_profile')
    @mock.patch('awsaudit.get_usernames', side_effect=_mock_get_usernames)
    @mock.patch('awsaudit.parse_args', side_effect=_mock_parse_args)
    def test_main(self, parse_args_mock, get_usernames_mock, set_profile_mock, export_to_csv_mock,
                  get_access_key_info_mock, get_mfa_status_mock):
        main('some user input args')
        parse_args_mock.assert_called_once_with({
        'description': 'Audit AWS IAM Users',
        'options': [{
            'short_option': '-f',
            'long_option': '--filename',
            'required': True,
            'help': 'specify the filename'
        },
            {
                'short_option': '-p',
                'long_option': '--profile',
                'required': True,
                'help': 'specify the AWS profile'
            }
        ]
    }, 'some user input args')
        get_usernames_mock.assert_called_once_with()
        set_profile_mock.assert_called_once_with('some profile')
        get_access_key_info_mock.assert_called_once_with('some usernames')
        get_mfa_status_mock.assert_called_once_with('some usernames')
        export_to_csv_mock.assert_has_calls([call('some access key info', 'some filename_AccessKeys.csv'),
                                             call('some mfa info', 'some filename_MFA.csv')])
