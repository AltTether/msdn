import os
import unittest

from msdn import Msdn

base_uri = 'https://hogehoge'
access_token = os.environ['MASTODON_ACCESS_TOKEN']
msdn = Msdn(base_uri, access_token)

class TestApi(unittest.TestCase):
    def test_accounts_id(self):
        response = msdn.accounts(id='30573')
        self.assertEqual(response.status_code, 200)
