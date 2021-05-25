from time import time


# structural patterns
# Декоратор
class UrlRoute:
    def __init__(self, routes, url):
        """
        Сохраняем значение переданного параметра
        """
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        """
        Вызов декоратора
        """
        self.routes[self.url] = cls()


# Декоратор для дебага
class TimeDebug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls):
        """
        Вызов декоратора, который считает сколько выполнялся метод
        """

        # это вспомогательная функция будет декорировать каждый отдельный метод класса, см. ниже
        def timeit(method):
            """
            нужен для того, чтобы декоратор класса wrapper обернул в timeit
            каждый метод декорируемого класса
            """
            def timed(*args, **kw):
                ts = time()
                result = method(*args, **kw)
                te = time()
                delta = te - ts
                print(f'debug --> {self.name} выполнялся {delta:2.2f} ms')
                return result
            return timed
        return timeit(cls)
