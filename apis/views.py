from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.views import View
from django.core.validators import validate_email, ValidationError
from django.contrib.auth import authenticate, login


class BaseView(View):
    @staticmethod
    def response(data={}, messange='',status=200):
        result = {
            'data':data,
            'message':messange,
        }
        return JsonResponse(result, status)


class UserCreateView(BaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwrags):
        return super(UserCreateView, self).dispatch(request, *args, ** kwrags)

    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(messange='아이디를 입력해주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(messange='패스워드를 입력해주세요.', status=400)
        email = request.POST.get('email', '')
        try:
            validate_email(email)
        except ValidationError:
            self.response(messange='올바른 이메일을 입력해주세요.', status=400)

        try:
            user = User.objects.create_user(username, email, password)
        except IntegrityError:
            return self.response(messange='이미 존재하는 아이디입니다.', status=400)

        return self.response({'user.id':user.id})

class UserLoginView(BaseView):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwrags):
        return super(UserLoginView, self).dispatch(request, *args, ** kwrags)
    def post(self, request):
        username = request.POST.get('username', '')
        if not username:
            return self.response(messange='아이디를 입력해주세요.', status=400)
        password = request.POST.get('password', '')
        if not password:
            return self.response(messange='패스워드를 입력해주세요.', status=400)
        user = authenticate(request, username=username, password=password)
        if user:
            return self.response(messange='입력 정보를 확인해주세요.', status=400)
        login(request, user)

        return self.response()