from urllib.parse import parse_qsl


# get requests
class GetRequests:
    @staticmethod
    def get_request_params(environ):
        # получаем параметры запроса
        query_string = environ['QUERY_STRING']
        # превращаем параметры в словарь
        request_params = parse_input_data(query_string)
        return request_params


# post requests
class PostRequests:
    @staticmethod
    def get_input_data_wsgi(env) -> bytes:
        # получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0
        # считываем данные, если они есть
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    @staticmethod
    def parse_input_data_wsgi(data: bytes) -> dict:
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = parse_input_data(data_str)
        return result

    def get_request_params(self, environ):
        # получаем данные
        data = self.get_input_data_wsgi(environ)
        # превращаем данные в словарь
        data = self.parse_input_data_wsgi(data)
        return data


def parse_input_data(data: str):
    """
    Получаем данные и разбираем их по параметрам
    """
    result = {}
    if data:
        params = parse_qsl(data)
        for param in params:
            result[param[0]] = param[1]
    return result
