from sys import version_info
from datetime import date
from views import Index, About, Gallery, Hello, CoursesList, \
    CreateCourse, CreateCategory, CategoryList, CloneCourse


# front controller
def front_secret(request):
    request['date'] = date.today()


def front_other(request):
    request['key'] = 'key'


def front_version(request):
    request['python_ver'] = f'{version_info.major}.{version_info.minor}'


fronts = [front_secret, front_other, front_version]

