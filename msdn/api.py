import json
import requests

from .actions import POST_ACTIONS, PATCH_ACTIONS


API_VERSION = 'v1'
API_ENDPOINT_START = 'api'

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
            if k in POST_ACTIONS:
                self.method = 'POST'
            if k in PATCH_ACTIONS:
                self.method = 'PATCH'

            return self.call_cls(access_token=self.access_token,
                                 call_cls=self.call_cls,
                                 uri=self.build_uri(self.uri, k),
                                 method=self.method)
    def __call__(self, **kargs):
        params = dict(kargs)

        if '_id' in self.uri:
            try:
                _id = params['_id']
                self.uri = self.uri.replace('_id', _id)
                del params['_id']
            except:
                print('_id params not found')

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

        headers = {'Authorization': 'Bearer ' + self.access_token}
        response = None
        if self.method == 'GET':
            response = requests.get(self.uri, headers=headers, params=params)
        elif self.method == 'POST':
            response = requests.post(self.uri, headers=headers, data=params)
        elif self.method == 'PATCH':
            response = requests.patch(self.uri, headers=headers, data=params)
        elif self.method == 'DELETE':
            response = requests.delete(self.uri, headers=headers, data=params)
        else:
            raise Exception()

        return response

    def build_uri(self, base, part):
        return base + '/' + part


class Msdn(MsdnCall):
    def __init__(self, base_uri, access_token):
        self.base_uri = base_uri
        self.access_token = access_token
        self.uri = self.build_uri(self.build_uri(base_uri, API_ENDPOINT_START), API_VERSION)
        super(Msdn, self).__init__(access_token=self.access_token,
                                   call_cls=MsdnCall,
                                   uri=self.uri)
