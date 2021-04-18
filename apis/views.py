from django.http import JsonResponse
from django.views import View

class BaseView(View):
    @staticmethod
    def response(data={}, messange='',status=200):
        result = {
            'data':data,
            'message':messange,
        }
        return JsonResponse(result, status)
