from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy

from adminapp.forms import ProductEditForm
from authapp.forms import ShopUserRegisterForm, ShopUserEditForm
from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView, UpdateView
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import connection
from django.db.models import F, Q


# def users(request):
#     title = 'админка/пользователи'
#
#     users_list = ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')
#     context = {
#         'title': title,
#         'objects': users_list,
#     }
#     return render(request, 'adminapp/users.html', context)

class UserListView(LoginRequiredMixin, ListView):
    model = ShopUser
    template_name = 'adminapp/users.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return ShopUser.objects.all().order_by('-is_active', '-is_superuser', '-is_staff', 'username')

    def get_context_data(self):
        context = super(UserListView, self).get_context_data()
        title = 'админка/пользователи'
        context.update({'title': title})

        return context


# def user_create(request):
#     title = 'пользователи/создание'
#
#     if request.method == 'POST':
#         user_form = ShopUserRegisterForm(request.POST, request.FILES)
#         if user_form.is_valid():
#             user_form.save()
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#
#     else:
#         user_form = ShopUserRegisterForm()
#
#     context = {
#         'title': title,
#         'update_form': user_form
#     }
#
#     return render(request, 'adminapp/user_update.html', context)

class UserCreateView(LoginRequiredMixin, CreateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    form_class = ShopUserRegisterForm
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self):
        context = super(UserCreateView, self).get_context_data()
        title = 'пользователи/создание'
        context.update({'title': title})

        return context



# def user_update(request, id):
#     title = 'профиль'
#     user = ShopUser.objects.get(id=id)
#     if request.method == 'POST':
#         edit_form = ShopUserEditForm(request.POST, request.FILES, instance=user)
#         if edit_form.is_valid():
#             edit_form.save()
#
#             return HttpResponseRedirect(reverse('admin_staff:users'))
#     else:
#         edit_form = ShopUserEditForm(instance=user)
#
#     context = {
#         'title': title,
#         'update_form': edit_form,
#     }
#     return render(request, 'adminapp/user_update.html', context)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = ShopUser
    template_name = 'adminapp/user_update.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_staff:users')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data()
        title = 'профиль'
        context.update({'title': title})

        return context


@user_passes_test(lambda u: u.is_superuser)
def user_delete(request, id):
    user = ShopUser.objects.filter(id=id)
    user.delete()
    return HttpResponseRedirect(reverse('admin_staff:users'))




@user_passes_test(lambda u: u.is_superuser)  # для контроля входа, только пользователи с флагом is_superuser
def categories(request):
    title = 'админка/категории'

    categories_list = ProductCategory.objects.all()

    content = {
        'title': title,
        'objects': categories_list
    }

    return render(request, 'adminapp/categories.html', content)


@user_passes_test(lambda u: u.is_staff)
def category_create(request):
    title = 'категории/создание'

    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            return HttpResponseRedirect(reverse('admin_staff:categories'))

    else:
        category_form = CategoryForm()

    context = {
        'title': title,
        'update_form': category_form
    }

    return render(request, 'adminapp/categories_update.html', context)


@user_passes_test(lambda u: u.is_staff)
def category_update(request, pk):
    title = 'категория'
    # user = ShopUser.objects.get(id=id)
    category = ProductCategory.objects.get(pk=pk)

    if request.method == 'POST':
        edit_form = CategoryForm(request.POST, request.FILES, instance=category)
        if edit_form.is_valid():
            edit_form.save()

            return HttpResponseRedirect(reverse('admin_staff:categories'))
    else:
        edit_form = CategoryForm(instance=category)

    context = {
        'title': title,
        'update_form': edit_form,
    }
    return render(request, 'adminapp/categories_update.html', context)



@user_passes_test(lambda u: u.is_staff)
def category_delete(request, pk):
    category = ProductCategory.objects.filter(pk=pk)
    category.delete()
    return HttpResponseRedirect(reverse('admin_staff:categories'))


def products(request, pk):
    title = 'админка/продукт'

    category = get_object_or_404(ProductCategory, pk=pk)
    products_list = Product.objects.filter(category__pk=pk).order_by('name')

    context = {
        'title': title,
        'category': category,
        'objects': products_list,
    }

    return render(request, 'adminapp/products.html', context)


def product_create(request, pk):
    title = 'продукты/создание'
    category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_form = ProductEditForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            return HttpResponseRedirect(reverse('adminapp:products', args=[pk]))
    else:
        product_form = ProductEditForm(initial={'category': category})

    context = {
        'title': title,
        'update_form': product_form,
        'category' : category,
    }
    return render(request, 'adminapp/product_update.html', context)




# def product_read(request, pk):
#     title = 'продукты/подробнее'
#     product = get_object_or_404(Product, pk=pk)
#
#     context = {
#         'title': title,
#         'product': product,
#     }
#     return render(request, 'adminapp/product_read.html', context)

class ProductDetailView(DetailView):
    model = Product
    template_name = 'adminapp/product_read.html'

    def get(self, request, *args, **kwargs):
        print(request)


def product_update(request, pk):
    title = 'продукты/редактирование'

    edit_product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        edit_form = ProductEditForm(request.POST, request.FILES, instance=edit_product)
        if edit_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('adminapp:product_update', args=[edit_product.pk]))
    else:
        edit_form = ProductEditForm(instance=edit_product)

    context = {
        'title': title,
        'update_form': edit_form,
        'category': edit_product.category,
    }
    return render(request, 'adminapp/product_update.html', context)


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        product.is_active = False if product.is_active else True
        product.save()
        return HttpResponseRedirect(reverse('adminapp:products', args=[product.category.pk]))

def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        if instance.is_active:
            instance.product_set.update(is_active=True)
        else:
            instance.product_set.update(is_active=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)