import os
import json
import unittest

from msdn import Msdn

base_uri = 'https://'
access_token = os.environ['MASTODON_ACCESS_TOKEN']
msdn = Msdn(base_uri, access_token)

test_id = ''

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

    def test_getting_account_followers(self):
        response = msdn.accounts._id.followers(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_getting_who_account_following(self):
        response = msdn.accounts._id.following(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_getting_account_statuses(self):
        response = msdn.accounts._id.statuses(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_following_unfollowing_account_reblogs(self):
        response = msdn.accounts._id.follow(_id=test_id)
        self.assertEqual(response.status_code, 200)
        response = msdn.accounts._id.unfollow(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_blocking_unblocking_account(self):
        response = msdn.accounts._id.block(_id=test_id)
        self.assertEqual(response.status_code, 200)
        response = msdn.accounts._id.unblock(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_muting_unmuting_account(self):
        response = msdn.accounts._id.mute(_id=test_id)
        mute_state = json.loads(response.text)['muting']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mute_state, True)
        response = msdn.accounts._id.unmute(_id=test_id)
        mute_state = json.loads(response.text)['muting']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mute_state, False)