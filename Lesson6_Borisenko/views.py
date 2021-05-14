from my_framework.templator import render
from patterns.my_creation_patterns import Engine, Logger
from patterns.my_structural_patterns import ExDecorator, DecoratorTimeit
from patterns.my_beh_patterns import EmailInfoNotification, SmsInfoNotification, ListView, CreateView, BaseSerializer

site = Engine()
logger = Logger('main')
email_notifier = EmailInfoNotification()
sms_notifier = SmsInfoNotification()

routes = {}


# контроллер - главная страница
@ExDecorator(routes=routes, url='/')
class Index:
    @DecoratorTimeit(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories, date=request.get('date', None),
                                python_ver=request.get('python_ver', None))


@ExDecorator(routes=routes, url='/about/')
class About:
    @DecoratorTimeit(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html', date=request.get('date', None))


@ExDecorator(routes=routes, url='/gallery/')
class Gallery:
    @DecoratorTimeit(name='Gallery')
    def __call__(self, request):
        return '200 OK', 'Gallery'


@ExDecorator(routes=routes, url='/hello/')
class Hello:
    @DecoratorTimeit(name='Hello')
    def __call__(self, request):
        return '200 OK', render('hello.html', username=request.get('request_params', {}).get('username'))


class NotFound404:
    @DecoratorTimeit(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список курсов
@ExDecorator(routes=routes, url='/courses-list/')
class CoursesList:
    @DecoratorTimeit(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('courses_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
@ExDecorator(routes=routes, url='/create-course/')
class CreateCourse:
    category_id = -1

    @DecoratorTimeit(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']
            name = data['name']
            name = site.decode_value(name)
            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                course = site.create_course('record', name, category)
                # Добавляем наблюдателей на курс
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)
                site.courses.append(course)
            return '200 OK', render('courses_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)
        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))
                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - копировать курс
@ExDecorator(routes=routes, url='/clone-course/')
class CloneCourse:
    @DecoratorTimeit(name='CloneCourse')
    def __call__(self, request):
        request_params = request['request_params']
        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'clone_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)
            return '200 OK', render('courses_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать категорию
@ExDecorator(routes=routes, url='/create-category/')
class CreateCategory:
    @DecoratorTimeit(name='CreateCategory')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
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
            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


# контроллер - список категорий
@ExDecorator(routes=routes, url='/category-list/')
class CategoryList:
    @DecoratorTimeit(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


@ExDecorator(routes=routes, url='/follower-list/')
class FollowerListView(ListView):
    queryset = site.followers
    template_name = 'follower_list.html'


@ExDecorator(routes=routes, url='/create-follower/')
class FollowerCreateView(CreateView):
    template_name = 'create_follower.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('follower', name)
        site.followers.append(new_obj)


@ExDecorator(routes=routes, url='/add-follower/')
class AddFollowerByCourseCreateView(CreateView):
    template_name = 'add_follower.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['followers'] = site.followers
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = site.decode_value(course_name)
        course = site.get_course(course_name)
        follower_name = data['follower_name']
        follower_name = site.decode_value(follower_name)
        follower = site.get_follower(follower_name)
        course.add_follower(follower)


@ExDecorator(routes=routes, url='/api/')
class CourseApi:
    @DecoratorTimeit(name='CourseApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.courses).save()
