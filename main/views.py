from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Category, Product


def product_list(request, category_slug=None):

    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    category = None

    #Фільтрація
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    #Пошук по назві
    query = request.GET.get('q')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    #Сортування
    sort = request.GET.get('sort')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name': 'name',
        'newest': '-created_at',  
    }
    if sort in sort_options:
        products = products.order_by(sort_options[sort])

    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'query': query,
        'sort': sort,
    }

    return render(request, 'main/product/list.html', context)


def product_detail(request, id, slug):
    """
    Відображає деталі продукту та пов'язані товари з тієї ж категорії.
    """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }

    return render(request, 'main/product/detail.html', context)
