import os
import json
import unittest

from msdn import Msdn

base_uri = 'https://'
access_token = os.environ['MASTODON_ACCESS_TOKEN']
msdn = Msdn(base_uri, access_token)

class TestApi(unittest.TestCase):
    def test_fetching_accounts(self):
        response = msdn.accounts._id(_id='30573')
        self.assertEqual(response.status_code, 200)

    def test_getting_current_user(self):
        response = msdn.accounts.verify_credentials()
        self.assertEqual(response.status_code, 200)

    def test_updating_current_user(self):
        response = msdn.accounts.update_credentials()
        self.assertEqual(response.status_code, 200)

    def test_updating_current_user_display_name(self):
        display_name = 'fugafuga'
        response = msdn.accounts.update_credentials(display_name=display_name)
        updated_display_name = json.loads(response.text)['display_name']
        self.assertEqual(updated_display_name, display_name)
