import random
import datetime
from math import ceil

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView, TemplateView

from client.models import ClientAccount, ProductOrderItem, ProductOrder, Invoice, InstallmentPay, InvoiceList
from stock.models import Product


# Create your views here.
class ClientList(ListView):
    model = ClientAccount
    ordering = ['-date']
    template_name = 'client/client.html'


class ClientAddView(CreateView):
    model = ClientAccount
    fields = '__all__'

    def get_success_url(self):
        return f"/client/profile/{self.object.pk}/"


class ClientProfile(DetailView):
    template_name = 'client/profile.html'
    model = ClientAccount

    def post(self, *args, **kwargs):
        model = self.request.POST.get('model')
        price = self.request.POST.get('price')
        quantity = self.request.POST.get('quantity')
        discount = self.request.POST.get('discount')
        client_user = self.get_object()
        product = Product.objects.get(model=model)
        if int(product.quantity) > 0:
            add_product = ProductOrderItem.objects.create(client=client_user, product=product, product_name=product.name, product_model=model, quantity=quantity, price=price, discount=discount)
            add_product.save()
        else:
            return redirect(self.request.get_full_path(), {'msg': 'Product Quantity Empty'})
        return redirect(self.request.get_full_path())

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(*args, **kwargs)

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client_user = self.get_object()
        client_add_product_list = ProductOrderItem.objects.filter(client=client_user).filter(is_order=False)

        context['product_list'] = client_add_product_list
        return context


def get_names(request):
    search = request.GET.get('search')
    payload = []
    if search:
        objs = Product.objects.filter(Q(name__icontains=search) | Q(model__icontains=search))
        for obj in objs:
            payload.append({
                'name': obj.name,
                'model_name': obj.model
            })
    return JsonResponse({
        'status': 200,
        'data': payload
    })


class ClientProfileUpdate(UpdateView):
    model = ClientAccount
    template_name = 'client/update.html'
    fields = '__all__'

    def get_success_url(self):
        return f"/client/profile/{self.object.pk}/"


class ProfileDelete(DeleteView):
    model = ClientAccount
    template_name = 'client/delete.html'

    def get_success_url(self):
        return "/client/"


class OrderCheckout(TemplateView):
    template_name = 'client/order.html'
    model = ProductOrder

    def product(self, *args, **kwargs):
        client_product = ProductOrderItem.objects.filter(client=self.kwargs['pk']).filter(is_order=False)
        total = sum([item.get_total for item in client_product])
        return total

    def post(self, *args, **kwargs):
        current_pay = self.request.POST.get('current_pay')
        total_amount = self.product()
        remaining = self.product() - float(current_pay)
        total_installment = self.request.POST.get('total_installment')
        installment_amount = ceil(remaining / float(total_installment))
        installment_method = self.request.POST.get('installment_method')
        installment_day = self.request.POST.get('installment_day')
        client = ClientAccount.objects.get(pk=self.kwargs['pk'])

        # Unique id Generator
        while True:
            random_number = random.randint(1000000000, 9999999999)
            if ProductOrder.objects.filter(unique_id=random_number).exists():
                continue
            else:
                break

        product_order = ProductOrder.objects.create(client=client, current_pay=current_pay, remaining_amount=remaining, installment_method=installment_method, installment_pay_day=installment_day, total_installment=total_installment,installment_amount=installment_amount, total_amount=total_amount, unique_id=random_number)
        product_order.save()

        # Get product order
        get_product_order = ProductOrder.objects.get(unique_id=random_number)

        # Invoice
        invoice = Invoice.objects.create(client=client, product_order=get_product_order, unique_id=random_number)
        invoice.save()
        get_invoice = Invoice.objects.get(product_order=get_product_order)

        client_product_list = ProductOrderItem.objects.filter(client=client).filter(is_order=False)

        # Stock quantity update
        for i in range(0, len(client_product_list)):
            product_list = client_product_list[i]
            product_model = getattr(product_list, 'product_model')
            quantity = getattr(product_list, 'quantity')
            product_get = Product.objects.get(model=product_model)
            product_quantity = int(product_get.quantity) - int(quantity)
            Product.objects.filter(model=product_model).update(quantity=product_quantity)

            # Invoice List
            invoice_list = InvoiceList.objects.create(invoice=get_invoice, product_item=product_list)
            invoice_list.save()

        # Product order confirm and set is_order field True
        client_product_list.update(is_order=True)

        # Installment Pay Class create
        now = datetime.datetime.now()
        weekday_index = int(installment_day)

        for i in range(int(total_installment)):

            if installment_method == "W":
                new_date = now + datetime.timedelta(weekday_index - now.weekday(), weeks=1)
                now = new_date
            elif installment_method == "M":
                new_date = now + datetime.timedelta(weekday_index - now.weekday(), hours=750)
                now = new_date

            installment_pay = InstallmentPay.objects.create(client=client, order=get_product_order, installment_pay_amount=installment_amount, day=installment_day, date=str(now)[:10])
            installment_pay.save()

        # return render(self.request, "client/invoice.html")
        return redirect("client:invoice_detail", pk=self.kwargs['pk'], int=random_number)
        # return redirect(self.request.get_full_path())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.product()
        return context


class InstallmentsView(TemplateView):
    template_name = 'client/installments.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        installment = ProductOrder.objects.filter(client=self.kwargs['pk'])
        context['total'] = installment
        return context


class InvoiceView(TemplateView):
    template_name = 'client/invoice.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        invoice = Invoice.objects.filter(client=self.kwargs['pk'])

        context['invoice_list'] = invoice
        return context


def invoice_detail(request, pk, int):
    if request.method == 'GET':
        try:
            invoice = Invoice.objects.filter(unique_id=int)
            context = {"invoice_list": invoice}
            return render(request, 'client/single-invoice.html', context)
        except ValueError as e:
            print(e)


