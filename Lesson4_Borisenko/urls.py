from sys import version_info
from datetime import date
import requests
from views import Index, About, Bitcoin, Hello, Ethereum, CoursesList, \
    CreateCourse, CreateCategory, CategoryList, CloneCourse


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


def version_front(request):
    request['python_ver'] = f'{version_info.major}.{version_info.minor}'


def btc_to_usd(request):
    try:
        request['btc_to_usd'] = requests.get('https://blockchain.info/ru/ticker').json().get('USD')['last']
    except Exception:
        request['btc_to_usd'] = 'Даже и не знаю какой курс..'


fronts = [secret_front, other_front, version_front, btc_to_usd]

routes = {
    '/': Index(),
    '/about/': About(),
    '/bitcoin/': Bitcoin(),
    '/hello/': Hello(),
    '/ethereum/': Ethereum(),
    '/course-list/': CoursesList(),
    '/create-course/': CreateCourse(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/clone-course/': CloneCourse(),
}
