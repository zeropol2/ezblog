from django.http import QueryDict
from django.http.multipartparser import MultiValueDict


class MoreMethodsMiddleware(object):
    def process_request(self, request):
        method = request.META.get('REQUEST_METHOD', '').upper()
        request.PUT = QueryDict('')
        request.DELETE = QueryDict('')
        request.PATCH = QueryDict('')

        if method not in ('PUT', 'PATCH', 'DELETE', ):
            return

        data, request._file = self._parse_request(request)
        setattr(request, method, data)

    def _parse_request(self, request):
        if request.META.get('CONTENT_TYPE', '').startswith('multipart'):
            return request.parse_file_upload(request.META, request)

        return QueryDict(request.body), MultiValueDict()