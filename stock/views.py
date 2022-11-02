from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from stock.models import Product


# Create your views here.

class ProductList(ListView):
    model = Product
    template_name = 'stock/productlist.html'


class ProductAddView(CreateView):
    model = Product
    fields = ('name', 'model', 'quantity', 'price')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return f"/stock/product/{self.object.pk}/"


class OneProduct(DetailView):
    template_name = 'stock/product.html'
    model = Product


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'stock/update.html'
    fields = ['name', 'model', 'quantity', 'price']

    def get_success_url(self):
        return f"/stock/product/{self.object.pk}/"


class ProductDelete(DeleteView):
    model = Product
    template_name = 'stock/delete.html'

    def get_success_url(self):
        return "/stock/"
