from excile_framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', date=request.get('date', None),
                                python_ver=request.get('python_ver', None),
                                btc_to_usd=request.get('btc_to_usd', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None))


class Bitcoin:
    def __call__(self, request):
        return '200 OK', 'Bitcoin'


class Etherium:
    def __call__(self, request):
        return '200 OK', 'Etherium'


class Hello:
    def __call__(self, request):
        return '200 OK', render('hello.html', username=request.get('username', None))


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
