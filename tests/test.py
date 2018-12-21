import os
import json
import base64
import unittest

import tests.config as config

from msdn import Msdn

base_uri = config.BASE_URI
access_token = config.ACCESS_TOKEN

msdn = Msdn(base_uri, access_token)

test_id = config.TEST_ID
test_domain = config.TEST_DOMAIN
test_filter_id = config.TEST_FILTER_ID
test_list_id = config.TEST_LIST_ID
test_notification_id = config.TEST_NOTIFICATION_ID
test_status_id = config.TEST_STATUS_ID

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
        response = msdn.accounts._id.unfollow(_id=test_id)
        self.assertEqual(response.status_code, 200)
        response = msdn.accounts._id.follow(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_blocking_unblocking_account(self):
        response = msdn.accounts._id.block(_id=test_id)
        self.assertEqual(response.status_code, 200)
        response = msdn.accounts._id.unblock(_id=test_id)
        self.assertEqual(response.status_code, 200)
        response = msdn.accounts._id.follow(_id=test_id)
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

    def test_endorsing_unendosing_account(self):
        response = msdn.accounts._id.pin(_id=test_id)
        endorse_state = json.loads(response.text)['endorsed']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(endorse_state, True)

    def test_getting_account_relationship(self):
        response = msdn.accounts.relationships(id=[test_id])
        self.assertEqual(response.status_code, 200)

    def test_searching_account(self):
        response = msdn.accounts.search(q='hoge',
                                        limit=1,
                                        following=False)
        self.assertEqual(response.status_code, 200)

    def test_apps(self):
        response = msdn.apps(client_name='hogehoge',
                             redirect_uris='urn:ietf:wg:oauth:2.0:oob',
                             scopes='read write follow')
        self.assertEqual(response.status_code, 200)

    def test_fetching_user_blocks(self):
        response= msdn.blocks(max_id=10000000,
                              since_id=0,
                              limit=80)
        self.assertEqual(response.status_code, 200)

    def test_fetching_user_domain_blocks(self):
        response = msdn.domain_blocks(max_id=100000000,
                                      since_id=0,
                                      limit=80)
        self.assertEqual(response.status_code, 200)

    def test_blocking_unblocking_domain(self):
        response = msdn.domain_blocks(domain=test_domain, _method='POST')
        self.assertEqual(response.status_code, 200)
        response = msdn.domain_blocks(domain=test_domain, _method='DELETE')
        self.assertEqual(response.status_code, 200)

    def test_fetching_endorsed_account(self):
        response = msdn.endorsements()
        self.assertEqual(response.status_code, 200)

    def test_fetching_user_favourite(self):
        response = msdn.favourites()
        self.assertEqual(response.status_code, 200)

    def test_fetching_filters(self):
        response = msdn.filters()
        self.assertEqual(response.status_code, 200)

    def test_creating_filters(self):
        response = msdn.filters(phrase='hoge piyo', context=['home'], _method='POST')
        self.assertEqual(response.status_code, 200)

    def test_getting_filters(self):
        response = msdn.filters._id(_id=test_filter_id)
        self.assertEqual(response.status_code, 200)

    def test_updating_filter(self):
        response = msdn.filters._id(_id=test_filter_id, phrase='fuga', _method='PUT')
        self.assertEqual(response.status_code, 200)

    def test_deleting_filter(self):
        response = msdn.filters._id(_id=test_filter_id)
        self.assertEqual(response.status_code, 200)

    def test_fetching_follow_requests(self):
        response = msdn.follow_requests()
        self.assertEqual(response.status_code, 200)

    def _authorizing_follow_request(self):
        response = msdn.follow_requests._id.authorize(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def _rejecting_follow_request(self):
        response = msdn.follow_requests._id.reject(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_fetching_follow_suggestion(self):
        response = msdn.suggestions()
        self.assertEqual(response.status_code, 200)

    def test_deleting_follow_suggestion(self):
        response = msdn.suggestions._id(_id=test_id, _method='DELETE')
        self.assertEqual(response.status_code, 200)

    def test_getting_current_instance_information(self):
        response = msdn.instance()
        self.assertEqual(response.status_code, 200)

    def test_getting_current_instance_custom_emojis(self):
        response = msdn.custom_emojis()
        self.assertEqual(response.status_code, 200)

    def test_retrieving_lists(self):
        response = msdn.lists()
        self.assertEqual(response.status_code, 200)

    def test_retrieving_lists_by_membership(self):
        response = msdn.accounts._id.lists(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_retrieving_accounts_in_list(self):
        response = msdn.lists._id.accounts(_id=test_list_id)
        self.assertEqual(response.status_code, 200)

    def test_retrieving_list(self):
        response = msdn.lists._id(_id=test_list_id)
        self.assertEqual(response.status_code, 200)

    def test_creating_updating_deleting_list(self):
        response = msdn.lists(title='hoge', _method='POST')
        self.assertEqual(response.status_code, 200)
        list_id = json.loads(response.text)['id']
        response = msdn.lists._id(_id=list_id, title='huga', _method='PUT')
        self.assertEqual(response.status_code, 200)
        response = msdn.lists._id(_id=list_id, _method='DELETE')
        self.assertEqual(response.status_code, 200)

    def test_adding_removing_accounts_to_list(self):
        response = msdn.lists._id.accounts(_id=test_list_id, account_ids=[test_id], _method='POST')
        self.assertEqual(response.status_code, 200)
        response = msdn.lists._id.accounts(_id=test_list_id, account_ids=[test_id], _method='DELETE')
        self.assertEqual(response.status_code, 200)


    def test_uploading_updating_media_attachment(self):
        response = msdn.media(_file='./tests/test_img/sample.jpg', _method='POST', description='hogehoge')
        self.assertEqual(response.status_code, 200)
        media_id = json.loads(response.text)['id']
        response = msdn.media._id(_id=media_id, description='hugahuga', _method='PUT')
        self.assertEqual(response.status_code, 200)

    def test_fetching_user_mutes(self):
        response = msdn.mutes()
        self.assertEqual(response.status_code, 200)

    def test_fetching_user_notifications(self):
        response = msdn.notifications(limit=1)
        self.assertEqual(response.status_code, 200)

    def test_fetching_single_notification(self):
        response = msdn.notifications._id(_id=test_notification_id)
        self.assertEqual(response.status_code, 200)

    def test_clearing_notifications(self):
        response = msdn.notifications.clear(_method='POST')
        self.assertEqual(response.status_code, 200)

    def test_dismissing_single_notification(self):
        response = msdn.notifications.dismiss(_method='POST')
        self.assertEqual(response.status_code, 200)

    def test_adding_push_subscription(self):
        public_key = ''
        auth_secret = base64.b64encode(os.urandom(16))
        endpoint = ''
        response = msdn.push.subscription(_method='POST',
                                          _endpoint=endpoint,
                                          public_key=public_key,
                                          auth_secret=auth_secret)
        self.assertEqual(response.status_code, 200)

    def test_getting_current_push_subscription_status(self):
        response = msdn.push.subscription()
        self.assertEqual(response.status_code, 200)

    def test_updating_push_subscription(self):
        response = msdn.push.subscription()
        self.assertEqual(response.status_code, 200)

    def test_removing_push_subscription(self):
        response = msdn.push.subscription(_method='DELETE')
        self.assertEqual(response.status_code, 200)

    def test_fetching_user_report(self):
        response = msdn.reports()
        self.assertEqual(response.status_code, 200)

    def test_reporting_user(self):
        response = msdn.reports(_method='POST')
        self.assertEqual(response.status_code, 200)

    def test_searching_content(self):
        response = msdn.search(q='hoge')
        self.assertEqual(response.status_code, 200)

    def test_fetching_status(self):
        response = msdn.statuses._id(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_getting_status_context(self):
        response = msdn.statuses._id.context(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_getting_card_associated_with_status(self):
        response = msdn.statuses._id.card(_id=test_id)
        self.assertEqual(response.status_code, 200)

    def test_getting_who_reblogged_favourited_status(self):
        response = msdn.statuses._id.reblogged_by(_id=test_status_id)
        self.assertEqual(response.status_code, 200)
        response = msdn.statuses._id.favourited_by(_id=test_status_id)
        self.assertEqual(response.status_code, 200)

    def test_posting_new_status(self):
        response = msdn.statuses(status='hogehoge', _method='POST')
        self.assertEqual(response.status_code, 200)

    def test_deleting_status(self):
        response = msdn.statuses._id(_id=test_status_id, _method='DELETE')
        self.assertEqual(response.status_code, 200)

    def test_reblogging_unreblogging_status(self):
        response = msdn.statuses._id.reblog(_id=test_status_id, _method='POST')
        self.assertEqual(response.status_code, 200)
        response = msdn.statuses._id.unreblog(_id=test_status_id, _method='POST')
        self.assertEqual(response.status_code, 200)

    def test_favouriting_unfavouriting_status(self):
        response = msdn.statuses._id.favourite(_id=test_status_id, _method='POST')
        self.assertEqual(response.status_code, 200)
        response = msdn.statuses._id.unfavourite(_id=test_status_id, _method='POST')
        self.assertEqual(response.status_code, 200)

    def test_pinning_unpinning_status(self):
        response = msdn.statuses._id.pin(_id=test_status_id, _method='POST')
        self.assertEqual(response.status_code, 200)
        response = msdn.statuses._id.unpin(_id=test_status_id, _method='POST')
        self.assertEqual(response.status_code, 200)

    def test_muting_unmuting_status(self):
        response = msdn.statuses._id.mute(_id=test_status_id, _method='POST')
        self.assertEqual(response.status_code, 200)
        response = msdn.statuses._id.unmute(_id=test_status_id, _method='POST')
        self.assertEqual(response.status_code, 200)

    def test_retrieving_home_timeline(self):
        response = msdn.timelines.home()
        self.assertEqual(response.status_code, 200)

    def test_retrieving_public_timeline(self):
        response = msdn.timelines.public()
        self.assertEqual(response.status_code, 200)

    def test_retrieving_hashtag_timeline(self):
        response = msdn.timelines.tag._hashtag(_hashtag='hoge')
        self.assertEqual(response.status_code, 200)

    def test_retrieving_list_timeline(self):
        response = msdn.timelines.list._listid(_listid=test_list_id)
        self.assertEqual(response.status_code, 200)

    def test_retrieving_direct_timeline(self):
        response = msdn.timelines.direct()
        self.assertEqual(response.status_code, 200)
