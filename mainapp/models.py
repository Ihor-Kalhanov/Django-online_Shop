from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class Catagory(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name of category')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True


    cateroty = models.ForeignKey('Catagory', verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Name of product')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Descrip', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        reversed(self.title)

class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name='Type of display')
    processor_freq = models.CharField(max_length=255, verbose_name='Processor')
    ram = models.CharField(max_length=255, verbose_name='OP')
    time_without_charge = models.CharField(max_length=255, verbose_name='Time battery')

    def __str__(self):
        return "{0} : {1}".format(self.cateroty.name, self.cateroty.title)

class  Smartphote(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name='Type of display')
    resolution = models.CharField(max_length=255, verbose_name='Pix of display')
    accum_volume = models.CharField(max_length=255, verbose_name='Battery')
    ram = models.CharField(max_length=255, verbose_name='OP')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='Max OP')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Main Camera')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Front Camera')

    def __str__(self):
        return "{0} : {1}".format(self.cateroty.name, self.cateroty.title)








class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='carts', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Final Price')

    def __str__(self):
        return "Product {0} (for busket)".format(self.product.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Owner', on_delete=models.CASCADE )
    products = models.ManyToManyField(CartProduct, related_name='carts', blank=True)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Final Price')

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone Number')
    address = models.CharField(max_length=255, verbose_name='Address')

    def __str__(self):
        return "Customer: {0} {1}".format(self.user.first_name, self.user.last_name)


