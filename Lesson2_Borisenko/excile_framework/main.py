import quopri
from excile_framework.requests import GetRequests, PostRequests


class PageNotFound:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


class Framework:

    """Класс Framework - основа фреймворка"""

    def __init__(self, routes_obj, fronts_obj):
        self.routes_lst = routes_obj
        self.fronts_lst = fronts_obj

    def __call__(self, environ, start_response):
        # получаем адрес, по которому выполнен переход
        path = environ['PATH_INFO']

        # добавление закрывающего слеша
        if not path.endswith('/'):
            path = f'{path}/'

        request = {}
        # Получаем все данные запроса добавлен пост и гет
        method = environ['REQUEST_METHOD']
        request['method'] = method

        if method == 'POST':
            data = PostRequests().get_request_params(environ)
            request['data'] = data
            print(f'POST-запрос: {Framework.decode_value(data)}')
        if method == 'GET':
            request_params = GetRequests().get_request_params(environ)
            request['request_params'] = request_params
            print(f'GET-запрос с параметрами: {request_params}')

        # находим нужный контроллер
        # отработка паттерна page controller
        if path in self.routes_lst:
            view = self.routes_lst[path]
        else:
            view = PageNotFound()
        # наполняем словарь request элементами
        # этот словарь получат все контроллеры
        # отработка паттерна front controller
        for front in self.fronts_lst:
            front(request)

        # запуск контроллера с передачей объекта request
        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_value(data):
        new_data = {}
        for key, value in data.items():
            new_value = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            value_decode_str = quopri.decodestring(new_value).decode('UTF-8')
            new_data[key] = value_decode_str
        return new_data
