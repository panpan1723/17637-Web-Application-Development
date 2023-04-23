from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from cmuplus.forms import *
# Imports the Item class
from cmuplus.models import *
from django.db.models import Q, Avg
from django.http import HttpResponse
import json
import random
from django.contrib.auth.decorators import login_required
from webapps.settings import BASE_DIR, CMUPLUS_USERS
from bootstrap_modal_forms.generic import BSModalCreateView

def _known_user_check(action_function):
    def my_wrapper_function(request, *args, **kwargs):
        if 'picture' not in request.session:
            request.session['picture'] = request.user.social_auth.get(provider='google-oauth2').extra_data['picture']

        if isinstance(CMUPLUS_USERS, str):
            if request.user.email.endswith(CMUPLUS_USERS):
                return action_function(request, *args, **kwargs)
            message = f"You must use an e-mail address ending with {CMUPLUS_USERS}"
            return render(request, 'cmuplus/main_page.html', {'message': message})
        else:
            assert isinstance(CMUPLUS_USERS, list)
            for pattern in CMUPLUS_USERS:
                if request.user.email == pattern:
                    return action_function(request, *args, **kwargs)
            message = "You're not authorized to use this application"
            return render(request, 'cmuplus/main_page.html', {'message': message})

    return my_wrapper_function

@login_required
@_known_user_check
def main_page(request):
    reversed_course_experience = reversed(CourseExperience.objects.all())
    if request.method == 'GET':
        return render(request, 'cmuplus/main_page.html', { 'course_experience': reversed_course_experience })

@login_required
@_known_user_check
def course_info(request, course_number):
    if request.method == "GET":
        context = {}
        # get course_number from main-page
        if course_number == "-1":
            course_num = str(request.GET.get('course_num', None)).strip()
        else:
            course_num = course_number
        course_exist = Course.objects.filter(course_number__exact=course_num)
        
        if len(course_exist) == 0:
            context['message'] = "Course of number " + str(course_num) + " does not exist."
            return render(request, 'cmuplus/course_info.html', context)
        else:
            course = CourseExperience.objects.filter(course_number__exact=course_num)
            load_list = course.values_list('load', flat=True)
            grad_satis_list = course.values_list('grade_satisfication', flat=True)
            difficulty_list = course.values_list('difficulty', flat=True)

            context['course_number'] = course_exist[0].course_number
            context['course_name'] = course_exist[0].course_name
            
            if len(course) > 0:
                context['credit'] = course[0].credit # assume the credit is unique
                context['professor_name']=[x.capitalize() for x in set(course.values_list('professor_lastname', flat=True))]
                context['load'] = list_average(load_list)
                context['grade_satis'] = list_average(grad_satis_list)
                context['difficulty'] = list_average(difficulty_list)
                context['course'] = course.order_by('-creation_time')
            else:
                context['credit'] = "N/A"
                context['professor_name']= [x.capitalize() for x in set(course_exist.values_list('professor_lastname', flat=True))]
                context['load'] = "N/A"
                context['grade_satis'] = "N/A"
                context['difficulty'] = "N/A"
                context['message'] = "No experiences posted."

            return render(request, 'cmuplus/course_info.html', context)
    
    # enter the page not by GET
    return redirect(reverse('main_page'))


def create_barchart(request, course_number):
    if request.method == "GET":
        datasets = []
        exp_has_grade = CourseExperience.objects.filter(course_number__exact=course_number).filter(~Q(grade=-1))

        semester = exp_has_grade.values_list('semester', flat=True)
        semester = list(set(semester)) #labels
        prof_lname = exp_has_grade.values_list('professor_lastname', flat=True)
        prof_lname = list(set(prof_lname))

        for p in prof_lname:
            data = {}
            num = []
            for s in semester:
                result = exp_has_grade.filter(Q(semester=s)).filter(Q(professor_lastname=p)).aggregate(Avg('grade'))
                if result is not None and result['grade__avg'] is not None:
                    if s not in data:
                        num.append(round(result['grade__avg'], 2))
                else:
                    num.append(0)
            data['label'] = p
            data['backgroundColor'] = random_color()
            data['data'] = num
            datasets.append(data)

        context = {}
        context['chart_data'] = {
            'labels': semester,
            'datasets': datasets
        }
        context = json.dumps(context)
        return HttpResponse(context)


def list_average(ls):
    int_ls = [int(x) for x in ls] # char is stored in db
    x = sum(int_ls)/len(ls)
    return round(x,1)


def random_color():
    rgb = [random.choice(range(256)) for i in range(3)]
    color = 'rgba('
    for c in rgb:
        color += str(c) + ','
    color += '0.5)'
    #rgba(0, 0, 0, 0.5)
    return color


@login_required
@_known_user_check
def post_experience(request):
    context = {}
    if request.method == 'GET':
        context['form'] = CourseExperienceForm()
        context['course_list'] = Course.objects.all()
        return render(request, 'cmuplus/post_experience.html', context)
    form = CourseExperienceForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        request.session['temp_data'] = form.errors['__all__'][0]
        #return render(request, 'cmuplus/post_experience.html', context)
        return redirect(reverse('post_experience'))


    new_experience = CourseExperience(
        created_by = request.user,
        creation_time=timezone.now(),
        course_number = form.cleaned_data['course_number'],
        course_name = form.cleaned_data['course_name'],
        semester = form.cleaned_data['semester'],
        credit = form.cleaned_data['credit'],
        load = form.cleaned_data['load'],
        grade_satisfication = form.cleaned_data['grade_satisfication'],
        difficulty = form.cleaned_data['difficulty'],
        subject = form.cleaned_data['subject'],
        is_anonymous = form.cleaned_data['is_anonymous'],

        professor_firstname = form.cleaned_data['professor_firstname'],
        professor_lastname = form.cleaned_data['professor_lastname'],
        grade = form.cleaned_data['grade'],
        content = form.cleaned_data['content'],
    )
    new_experience.save()

    return redirect(reverse('main_page'))


@login_required
@_known_user_check
def discussion_board(request):
    context = {}

    if request.method == "GET":
        context['form'] = PostForm()
        context['commentform'] = CommentForm()
        context['items'] = Post.objects.all().order_by("-creation_time")
        return render(request, 'cmuplus/discussion_board.html', context)
    
    form = PostForm(request.POST)
    context['form'] = form

    # validates
    if not form.is_valid():
        return render(request, 'cmuplus/discussion_board.html', context)

    post = Post()
    post.user = request.user
    post.title = form.cleaned_data['title']
    post.text = form.cleaned_data['text']
    post.creation_time = timezone.now()
    
    post.save()
    
    # create new discussion board data
    return redirect(reverse('discussion_board'))

@login_required
@_known_user_check
def post_info(request, post_id):
    context = {}

    if request.method == "GET":
        context['post_id'] = post_id
        context['post'] = Post.objects.get(id=post_id)
        context['form'] = CommentForm()
        context['items'] = Post.objects.get(id=post_id).comments.all().order_by("-creation_time")
        context['numComment'] = Post.objects.get(id=post_id).comments.count()
        return render(request, 'cmuplus/post_info.html', context)
    
    form = CommentForm(request.POST)
    context['form'] = form
    context['post_id'] = post_id
    post = Post.objects.get(id=post_id)

    # validation
    if not form.is_valid():
        return render(request, 'cmuplus/post_info.html', context)

    comment = Comment()
    comment.text = form.cleaned_data['text']
    comment.creation_time = timezone.now()
    comment.user = request.user

    comment.save()

    post.comments.add(comment)

    post.save()
    context['post'] = post
    context['items'] = post.comments.all().order_by("-creation_time")
    context['numComment'] = Post.objects.get(id=post_id).comments.count()

    return render(request, 'cmuplus/post_info.html', context)

@login_required
@_known_user_check
def display_experience(request, course_experience_id):
    current_course_experience = get_object_or_404(CourseExperience, id=course_experience_id)
    #reversed(CourseExperience.objects.all())
    if request.method == 'GET':
        return render(request, 'cmuplus/display_experience.html', { 'course_experience': current_course_experience })
