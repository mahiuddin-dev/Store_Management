from django.db import models

from stock.models import Product


# Create your models here.
class ClientAccount(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    care_of = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=14)
    village = models.CharField(max_length=255)
    upazila = models.CharField(max_length=255)
    zila = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_absolute_url(self):
        return f"profile/{self.pk}/"


class ProductOrder(models.Model):

    PAYMENT_METHOD_WEAKLY = 'W'
    PAYMENT_METHOD_MONTHLY = 'M'

    PAYMENT_METHOD = [
        (PAYMENT_METHOD_WEAKLY, 'Weakly'),
        (PAYMENT_METHOD_MONTHLY, 'Monthly'),
    ]

    INSTALLMENT_SUNDAY = '6'
    INSTALLMENT_MONDAY = '0'
    INSTALLMENT_TUESDAY = '1'
    INSTALLMENT_WEDNESDAY = '2'
    INSTALLMENT_THURSDAY = '3'
    INSTALLMENT_FRIDAY = '4'
    INSTALLMENT_SATURDAY = '5'

    INSTALLMENT_PAY = [
        (INSTALLMENT_SUNDAY, 'Sunday'),
        (INSTALLMENT_MONDAY, 'Monday'),
        (INSTALLMENT_TUESDAY, 'Tuesday'),
        (INSTALLMENT_WEDNESDAY, 'Wednesday'),
        (INSTALLMENT_THURSDAY, 'Thursday'),
        (INSTALLMENT_FRIDAY, 'Friday'),
        (INSTALLMENT_SATURDAY, 'Saturday'),
    ]

    client = models.ForeignKey(ClientAccount, on_delete=models.PROTECT)
    current_pay = models.IntegerField()
    remaining_amount = models.IntegerField()
    installment_method = models.CharField(max_length=1, choices=PAYMENT_METHOD, default=PAYMENT_METHOD_WEAKLY)
    installment_pay_day = models.CharField(max_length=1, choices=INSTALLMENT_PAY, default=INSTALLMENT_FRIDAY)
    total_installment = models.PositiveIntegerField()
    installment_amount = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField(blank=True, null=True)
    unique_id = models.PositiveIntegerField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.client.first_name, self.client.last_name)


class ProductOrderItem(models.Model):
    client = models.ForeignKey(ClientAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(ProductOrder,  on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    product_model = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField()
    discount = models.IntegerField()
    order_added = models.DateTimeField(auto_now_add=True)
    is_order = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.product_name+" -> " + '{} {}'.format(self.client.first_name, self.client.last_name)

    @property
    def get_total(self):
        total = 0
        if self.discount > 0:
            actual = self.price - (self.price*self.discount)/100
            total += self.quantity * actual
        else:
            total += self.quantity * self.price

        return total


class InstallmentPay(models.Model):
    client = models.ForeignKey(ClientAccount, on_delete=models.PROTECT)
    order = models.ForeignKey(ProductOrder, on_delete=models.PROTECT)
    installment_pay_amount = models.PositiveIntegerField(default=0)
    date = models.DateField()
    day = models.CharField(max_length=20)
    is_pay = models.BooleanField(default=False, blank=True, null=True)
    is_late = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.client.last_name


class Invoice(models.Model):
    client = models.ForeignKey(ClientAccount, on_delete=models.CASCADE)
    product_order = models.ForeignKey(ProductOrder, on_delete=models.CASCADE)
    unique_id = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return self.product_order.client.last_name


class InvoiceList(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product_item = models.ForeignKey(ProductOrderItem, on_delete=models.CASCADE)

    def __str__(self):
        return self.invoice.product_order.client.last_name

