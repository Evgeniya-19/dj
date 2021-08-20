from django.conf import settings
from django.db import models


from mainapp.models import Product

class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0,
    )

    add_datetime = models.DateTimeField(
        verbose_name='время',
        auto_now_add=True,
    )

    @property
    def product_cost(self):
        return self.product.price * self.quantity


    @property
    def total_quantity(self):
        items = Basket.objects.filter(user=self.user)
        totalquantity =sum(list(map(lambda x:x.quantity, items)))
        return totalquantity

    @property
    def total_cost(self):
        items = Basket.objects.filter(user=self.user)
        totalcost = sum(list(map(lambda x: x.product_cost, items)))
        return totalcost