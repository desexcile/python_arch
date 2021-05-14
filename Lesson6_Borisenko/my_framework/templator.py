from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """

    my_env = Environment()
    my_env.loader = FileSystemLoader(folder)
    template = my_env.get_template(template_name)
    return template.render(**kwargs)

