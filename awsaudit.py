from src.argutils import parse_args
from src.awsutils import get_usernames, set_profile, get_access_key_info, get_mfa_status
from src.csvutils import export_to_csv
import sys


UI_CONFIG = {
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
    }


def main(user_input_args):
    user_args = parse_args(UI_CONFIG, user_input_args)
    set_profile(user_args.profile)
    users = get_usernames()
    export_to_csv(get_access_key_info(users), f'{user_args.filename}_AccessKeys.csv')
    export_to_csv(get_mfa_status(users), f'{user_args.filename}_MFA.csv')


if __name__ == '__main__':
    main(sys.argv[1:])
