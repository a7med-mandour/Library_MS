from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from .froms import *
from django.db.models import Sum, F


# Create your views here.


def books(request):
    search_query = request.GET.get('search_name')
    if search_query:
        search_book = Book.objects.filter(title__icontains= search_query)
    else:
        search_book = Book.objects.all()



    # books = Book.objects.all()
    category = Category.objects.all()

    if request.method =="POST":
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            return redirect('books')
    else:
        cat_form = CategoryForm()   
        
    context = {
        'books':search_book,
        'category':category,
        'cat_form':cat_form,

    }
    return render(request, 'pages/books.html', context)

################################################################

def index(request):

    if request.method =="POST":
        book_form = BookForm(request.POST, request.FILES)
        if book_form.is_valid():
            book_form.save()
            return redirect('/')
        # else:
        #  print("Form is invalid:", book_form.errors)
        cat_form = CategoryForm(request.POST)
        if cat_form.is_valid():
            cat_form.save()
            return redirect('/')
        
    else:
        book_form = BookForm() 
        cat_form = CategoryForm()

    books = Book.objects.all()
    category = Category.objects.all()
    available = Book.objects.filter( status = 'available')
    rental = Book.objects.filter( status = 'rental')
    sold = Book.objects.filter( status = 'sold')

    rental_book = rental.annotate(total_rental = F('rental_price_day')* F('rental_period'))
    rental_price = rental_book.aggregate(Sum('total_rental'))['total_rental__sum'] or 0
    sold_price = sold.aggregate(Sum('price'))['price__sum'] or 0

    total_gain = sold_price + rental_price 



    context = {
        'books':books,
        'category':category,
        'form':book_form,
        'cat_form':cat_form,
        'books_count':books.count(),
        'available': available,
        'rental':rental,
        'rental_price':rental_price,
        'sold':sold,
        'sold_price':sold_price,
        'total_gain':total_gain

    }
    
    return render(request, 'pages/index.html', context)


def delete(request,book_name):
    book = get_object_or_404(Book,title=book_name )
    if request.method =='POST':
        book.delete()
        return redirect('/')
    return render(request, 'pages/delete.html')


def update(request,book_name):
    book = get_object_or_404(Book, title=book_name)
    if request.method=="POST":
        book_form = BookForm(request.POST,request.FILES,instance=book)
        
        if book_form.is_valid():
            book_form.save()
            return redirect('index')
    else:
        book_form = BookForm(instance=book)
    return render(request, 'pages/update.html',{'book_form':book_form})