import json

from requests import Request, Session


API_VERSION = 'v1'
API_ENDPOINT_START = 'api'

class MsdnCall(object):
    def __init__(self, access_token=None, call_cls=None, uri=None):
        self.access_token = access_token
        self.call_cls = call_cls
        self.uri = uri

    def __getattr__(self, k):
        try:
            object.__getattr__(self, k)
        except AttributeError:
            return self.call_cls(access_token=self.access_token,
                                 call_cls=self.call_cls,
                                 uri=self.build_uri(self.uri, k))
    def __call__(self, **kargs):
        params = dict(kargs)

        session = Session()
        request = Request('GET', self.uri)
        prepare_request = session.prepare_request(request)

        prepare_request.headers['Authorization'] = 'Bearer ' + self.access_token
        prepare_request.params = params

        response = session.send(prepare_request)
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
