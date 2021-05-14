from time import time


# structural patterns
# Декоратор
class ExDecorator:
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
class DecoratorTimeit:

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
                t_start = time()
                result = method(*args, **kw)
                t_end = time()
                delta = t_end - t_start

                print(f'debug --> {self.name} занял {delta:2.2f} ms на выполнение')
                return result
            return timed
        return timeit(cls)
