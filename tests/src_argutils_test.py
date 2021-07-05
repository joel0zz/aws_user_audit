from src.argutils import parse_args
from unittest import TestCase

config = {
        'description': 'Test tester',
        'options': [{
            'short_option': '-t',
            'long_option': '--testboy',
            'required': True,
            'help': 'do you still work?'
        },
            {
                'short_option': '-p',
                'long_option': '--pls',
                'required': True,
                'help': 'pls still work'
            }
        ]
    }


class TestArgUtils(TestCase):
    def test_parser(self):
        parser = parse_args(config, ['-t', 'iamworking', '-p', 'plsmister'])
        self.assertEqual(parser.testboy, 'iamworking')
        self.assertEqual(parser.pls, 'plsmister')



