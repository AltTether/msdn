import os
import json
import base64
import requests

from .actions import POST_ACTIONS, PATCH_ACTIONS


API_VERSION = 'v1'
ENDPOINT_START_TOKEN = 'api'

class MsdnCall(object):
    def __init__(self, access_token=None, call_cls=None, uri=None, method='GET'):
        self.access_token = access_token
        self.call_cls = call_cls
        self.uri = uri
        self.method = method

    def __getattr__(self, k):
        try:
            object.__getattr__(self, k)
        except AttributeError:

            method = self.method
            if k in POST_ACTIONS:
                method = 'POST'
            if k in PATCH_ACTIONS:
                method = 'PATCH'

            return self.call_cls(access_token=self.access_token,
                                 call_cls=self.call_cls,
                                 uri=self.build_uri(self.uri, k),
                                 method=method)

    def __call__(self, **kargs):
        params = dict(kargs)
        files = dict()

        if '_file' in params:
            have_file = True
            file_path = params['_file']
            file_name = os.path.basename(file_path)
            _, file_extension = os.path.splitext(file_name)
            _file = None
            with open(file_path, 'rb') as f:
                _file = f.read()
            if file_extension == 'jpg':
                file_extension = 'jpeg'
            files['file'] = (file_name, _file, 'image/' + file_extension)
            del params['_file']

        if 'auth_secret' in params and 'public_key' in params and '_endpoint' in params:
            params['subscription[endpoint]'] = params['_endpoint']
            params['subscription[keys][p256dh]'] = params['public_key']
            params['subscription[keys][auth]'] = params['auth_secret']
            del params['_endpoint']
            del params['public_key']
            del params['auth_secret']

        if '_id' in self.uri:
            try:
                _id = params['_id']
                self.uri = self.uri.replace('_id', _id)
                del params['_id']
            except:
                raise Exception('_id params not found')

        if '_hashtag' in self.uri:
            try:
                hashtag = params['_hashtag']
                self.uri = self.uri.replace('_hashtag', hashtag)
                del params['_hashtag']
            except:
                raise Exception('_hashtag params not found')

        if '_listid' in self.uri:
            try:
                list_id = params['_listid']
                self.uri = self.uri.replace('_listid', list_id)
                del params['_listid']
            except:
                raise Exception('_listid params not found')

        if '_method' in params:
            self.method = params['_method']
            del params['_method']

        for key, value in params.items():
            if type(value) is bool:
                params[key] = 'true' if value else 'false'

            if "[]" in key:
                continue
            if type(value) is list:
                params[key+"[]"] = value
                del params[key]

        stream = False
        if 'streaming' in self.uri:
            stream = True

        headers = {'Authorization': 'Bearer ' + self.access_token}
        response = None
        if self.method == 'GET':
            response = requests.get(self.uri, headers=headers, params=params, stream=stream)
        elif self.method == 'PUT':
            response = requests.put(self.uri, headers=headers, params=params)
        elif self.method == 'POST':
            response = requests.post(self.uri, headers=headers, data=params, files=files)
        elif self.method == 'PATCH':
            response = requests.patch(self.uri, headers=headers, data=params)
        elif self.method == 'DELETE':
            response = requests.delete(self.uri, headers=headers, data=params)
        else:
            raise Exception()

        return response

    def build_uri(self, base, part):
        return base + '/' + part

    def reset_method(self):
        self.method = 'GET'


class Msdn(MsdnCall):
    def __init__(self, base_uri, access_token, api_version=API_VERSION, endpoint_start_token=ENDPOINT_START_TOKEN):
        self.base_uri = base_uri
        self.access_token = access_token
        self.uri = self.build_uri(base_uri, endpoint_start_token)
        self.uri = self.build_uri(self.uri, api_version)
        super(Msdn, self).__init__(access_token=self.access_token,
                                   call_cls=MsdnCall,
                                   uri=self.uri)
