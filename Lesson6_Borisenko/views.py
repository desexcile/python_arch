from excile_framework.templator import render
from patterns.excile_creation_patterns import Engine, Logger
from patterns.excile_structural_patterns import UrlRoute, TimeDebug
from patterns.excile_beh_patterns import EmailInfoNotification, SmsInfoNotification,\
    ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
routes = {}
email_notifier = EmailInfoNotification()
sms_notifier = SmsInfoNotification()


@UrlRoute(routes=routes, url='/')
class Index:
    @TimeDebug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html',
                                date=request.get('date', None),
                                python_ver=request.get('python_ver', None),
                                btc_to_usd=request.get('btc_to_usd', None))


@UrlRoute(routes=routes, url='/about/')
class About:
    @TimeDebug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html',
                                date=request.get('date', None),
                                btc_to_usd=request.get('btc_to_usd', None))


@UrlRoute(routes=routes, url='/bitcoin/')
class Bitcoin:
    @TimeDebug(name='Bitcoin')
    def __call__(self, request):
        return '200 OK', str(request.get('btc_to_usd', None))


@UrlRoute(routes=routes, url='/ethereum/')
class Ethereum:
    @TimeDebug(name='Ethereum')
    def __call__(self, request):
        return '200 OK', 'Ethereum'


@UrlRoute(routes=routes, url='/hello/')
class Hello:
    @TimeDebug(name='Hello')
    def __call__(self, request):
        return '200 OK', render('hello.html',
                                username=request.get('request_params', {}).get('username'),
                                btc_to_usd=request.get('btc_to_usd', None))


class NotFound404:
    @TimeDebug(name='404NotFound')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@UrlRoute(routes=routes, url='/course-list/')
class CoursesList:
    @TimeDebug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            print(request)
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    btc_to_usd=request.get('btc_to_usd', None))
        except KeyError:
            return '200 OK', '0 Courses'


@UrlRoute(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @TimeDebug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    btc_to_usd=request.get('btc_to_usd', None))
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                return '200 OK', render('create_course.html',
                                        name=category.name,
                                        id=category.id,
                                        btc_to_usd=request.get('btc_to_usd', None))
            except KeyError:
                return '200 OK', 'Category 0'


@UrlRoute(routes=routes, url='/clone-course/')
class CloneCourse:
    @TimeDebug(name='CloneCourse')
    def __call__(self, request):
        request_params = request['request_params']
        try:
            print(request)
            name = request_params['name']
            cat_name = request_params['cat']
            cat_id = request_params['id']
            category = site.find_category_by_id(int(cat_id))
            old_course = site.get_course(name)
            if old_course:
                new_name = f'clone_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                category.courses.append(new_course)
                site.courses.append(new_course)
            return '200 OK', render('course_list.html',
                                    objects_list=category.courses,
                                    name=cat_name,
                                    id=category.id,
                                    btc_to_usd=request.get('btc_to_usd', None))
        except KeyError:
            return '200 OK', 'No courses have been added yet'


@UrlRoute(routes=routes, url='/create-category/')
class CreateCategory:
    @TimeDebug(name='CreateCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            print(request)
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category_id = data.get('category_id')
            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))
            new_category = site.create_category(name, category)
            site.categories.append(new_category)
            return '200 OK', render('category_list.html',
                                    objects_list=site.categories,
                                    btc_to_usd=request.get('btc_to_usd', None))
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories,
                                    btc_to_usd=request.get('btc_to_usd', None))


@UrlRoute(routes=routes, url='/category-list/')
class CategoryList:
    @TimeDebug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories,
                                btc_to_usd=request.get('btc_to_usd', None))


@UrlRoute(routes=routes, url='/preminer-list/')
class PreMinersListView(ListView):
    queryset = site.preminers
    template_name = 'preminer_list.html'


@UrlRoute(routes=routes, url='/create-preminer/')
class PreMinerCreateView(CreateView):
    template_name = 'create_preminer.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('preminer', name)
        site.preminers.append(new_obj)


@UrlRoute(routes=routes, url='/add-preminer/')
class AddPreMinerByCourseCreateView(CreateView):
    template_name = 'add_preminer.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['preminers'] = site.preminers
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        preminer_name = data['preminer_name']
        preminer_name = site.decode_value(preminer_name)
        preminer = site.get_preminer(preminer_name)
        course.add_preminer(preminer)


@UrlRoute(routes=routes, url='/api/')
class CourseApi:
    @TimeDebug(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
