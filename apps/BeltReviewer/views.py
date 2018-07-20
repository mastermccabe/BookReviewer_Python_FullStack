from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.messages import *
from django.db.models import Avg
from django.core.urlresolvers import reverse
import bcrypt

def index(request):
    if 'user_id' not in request.session:
        return render(request,"BeltReviewer/index.html")
    else:
        request.session['user_id']=request.session['user_id']
        user_id=request.session['user_id']
        print user_id
        messages.add_message(request, INFO ,"Signed in:",user_id)
        return redirect('/success')
    print "index"
    return render(request,"BeltReviewer/index.html")

def register(request):
    errors = Users.objects.validChecker(request.POST)
    if len(errors)==0:
        for u in Users.objects.all():
            if u.email == request.POST['email']:
                messages.add_message(request, INFO ,"email already taken, try logging in")

                return redirect('/')
        user = Users.objects.create(name=request.POST["name"],alias=request.POST["alias"],email=request.POST["email"],password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session['user_id'] = user.id
        print request.session['user_id']
        # messages.add_message(request, INFO ,"success")
        return redirect('/success')
    else:
        for i in errors:
            messages.add_message(request, INFO , errors[i])
        return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        messages.add_message(request, INFO ,"Please log in")
        return redirect('/')


    if 'user_id' in request.session:
        context = {
        "user":Users.objects.get(id=request.session['user_id']),
        "user_list":Users.objects.all(),
        }

        messages.add_message(request, INFO ,"Success")
        return redirect('/books')
        return render(request,"BeltReviewer/books.html", context)

def books(request):
    if 'user_id' not in request.session:
        messages.add_message(request, INFO ,"Please log in")
        return redirect('/')


    if 'user_id' in request.session:
        context = {
        "user":Users.objects.get(id=request.session['user_id']),
        "user_list":Users.objects.all(),

        "review_list":Reviews.objects.order_by('-created_at'),

        "book_list":Books.objects.all(),
        # "average":Reviews.objects.all().aggregate(Avg('rating')),
        "author":Authors.objects.all()
        }
        print context['book_list']
# Books.objects.get(id=author_list_id).author_list.author_name
        messages.add_message(request, INFO ,"Success")
        return render(request,"BeltReviewer/books.html", context)

def add_review(request, book_id):
    print book_id
    if 'user_id' in request.session:
        if request.method=='POST':

            context = {
            "user":Users.objects.get(id=request.session['user_id']),
            "review": Reviews.objects.create(review=request.POST['review'],reviewed_book_id=book_id,user_reviews_id=request.session['user_id'],rating=int(request.POST['rating'])),
                }
    return redirect('/books/'+book_id, context)



def book_review(request, book_id):

    if 'user_id' not in request.session:
        messages.add_message(request, INFO ,"Please log in")
        return redirect('/')
    if 'user_id' in request.session:
        context = {
        "user":Users.objects.get(id=request.session['user_id']),
        "user_list":Users.objects.all(),

        "review_list":Reviews.objects.filter(reviewed_book_id=book_id),
        "average":Reviews.objects.filter(reviewed_book_id=book_id).aggregate(Avg('rating')),
        "rating":Reviews.objects.filter(reviewed_book_id=book_id),
        "book_list":Books.objects.get(id=book_id),
        "author":Authors.objects.all()
        }

        return render(request,"BeltReviewer/book_review.html", context)

def users(request):

    if 'user_id' in request.session:
        context = {
        'users':Users.objects.all(),
        "user":Users.objects.get(id=request.session['user_id']),
        "authors":Authors.objects.all(),

        }

    return render(request,'BeltReviewer/view_users.html', context)


def show(request, user_id):
    if 'user_id' in request.session:
        context = {
        'users':Users.objects.get(id=user_id),
        "user":Users.objects.get(id=request.session['user_id']),


        }

    # user = {'user': Users.objects.get(id=user_id)}

    return render(request,'BeltReviewer/show_user.html', context)



def edit(request, user_id):
    if 'user_id' in request.session:
        context = {
        'users':Users.objects.get(id=user_id),
        "user":Users.objects.get(id=request.session['user_id']),

        }
    if request.method=='POST':

        # Users.objects.filter(u).update(name="updated user",alias="user alias",email="new_email@yahoo.com")
        Users.objects.filter(id=user_id).update(name=request.POST['name'],alias=request.POST['alias'])
        # return redirect('/users/'+user_id, context, updated_user)

        return redirect('/users/'+user_id)
    return render(request,'BeltReviewer/edit_user.html', context)




def add(request):
    if 'user_id' not in request.session:
        messages.add_message(request, INFO ,"Please log in")
        return redirect('/')
    if 'user_id' in request.session:
        context = {
        "user":Users.objects.get(id=request.session['user_id']),
        "authors":Authors.objects.all(),

        }
    if request.method=='POST':
        print "line 88"
        # if (request.POST['auth_dropdown'] is None and len(request.POST['author_text']))<4:
        #     messages.add_message(request, ERROR ,"Must fill out one of the author choices above (no authors less than 4 characters)")
        if len(request.POST['author_text'])>4:
            for a in Authors.objects.all():
                if a.author_name == request.POST['author_text']:
                    print "in existing author text"
                    messages.add_message(request, ERROR ,"Author already exists")
                    return redirect('/books/add')
            print "new author id"
            author=Authors.objects.create(author_name=request.POST['author_text'])
            new_book=Books.objects.create(title=request.POST['title'],author_list_id=author.id,uploader_id=request.session['user_id'])
            messages.add_message(request, INFO ,"Success")
            if request.POST['rating'] == None:
                messages.add_message(request, Error ,"Please add a rating")
                return redirect('/books/add')
            else:
                review = Reviews.objects.create(review=request.POST['review'],reviewed_book_id=new_book.id,user_reviews_id=request.session['user_id'],rating=int(request.POST['rating']))
                return redirect('/books/')
        elif request.POST['auth_dropdown'] > 1:
            new_book=Books.objects.create(title=request.POST['title'],author_list_id=request.POST['auth_dropdown'],uploader_id=request.session['user_id'])
            rating = request.POST['review']
            print 'rating' , rating
            # Reviews.objects.create(review="impresive work",reviewed_book_id=1,user_reviews_id=1,rating=5)
            if request.POST['rating'] == None:
                messages.add_message(request, Error ,"Please add a rating")
                return redirect('/books/add')
            else:
                review = Reviews.objects.create(review=request.POST['review'],reviewed_book_id=new_book.id,user_reviews_id=request.session['user_id'],rating=int(request.POST['rating']))
                messages.add_message(request, INFO ,"Success")
            return redirect('/books/')
    #  if (request.POST['author_text'] != None and request.POST['auth_dropdown'] != None):
    #      messages.add_message(request, ERROR ,"Please select from either List or Author not both")
    #      return redirect('/books/add')


            # new_book = Books.objects.create(title=request.POST["title"],alias=request.POST["alias"],email=request.POST["email"],password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
    context = {
    "user":Users.objects.get(id=request.session['user_id']),
    "user_list":Users.objects.all(),
    "review_list":Reviews.objects.all(),

    "book_list":Books.objects.all(),
    "authors":Authors.objects.all()}

    return render(request,"BeltReviewer/addbooks.html", context)

def login(request):
    user_list = Users.objects.all()
    for u in user_list:
        if u.email == request.POST['email'] and bcrypt.checkpw(request.POST['password'].encode(),u.password.encode()):
            request.session['user_id'] = u.id
            return redirect('/success')
    messages.add_message(request, INFO, "Invalid password or email, or both")
    request.session.clear()
    print "session cleared"
    return redirect('/books')

def delete(request, user_id):
    Books.objects.get(id=user_id).delete()

    return redirect('/books')

def clearsession(request):
    request.session.clear()
    messages.add_message(request, INFO ,"Logged out")
    return redirect('/')
