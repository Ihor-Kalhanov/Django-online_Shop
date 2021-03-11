from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()



def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reversed(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})



class MinResolutionErrorException(Exception):
    pass

class MaxResolutionErrorException(Exception):
    pass


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.first(model_in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_maneger.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(models=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__.meta.model_name.startwith(with_respect_to), reverse=True
                    )
        return products

class LatestProducts:

    objects = LatestProductsManager()

class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Notebook':'notebook__count',
        'Smartphone': 'smartphone__count'
    }

    def get_quereset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('notebook', 'smartphone')
        qs =  list(self.get_quereset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c,self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Name of category')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    MIN_RESOLUTION = (400, 400)
    MAX_RESOLUTION = (800, 800)
    MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True


    category = models.ForeignKey('Category', verbose_name='Category', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Name of product')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Image')
    description = models.TextField(verbose_name='Descrip', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        image = self.image
        img = Image.open(image)
        min_height, min_width = self.MIN_RESOLUTION
        max_height, max_width = self.MAX_RESOLUTION
        if img.height < min_height or img.width < min_width:
            raise MinResolutionErrorException('Your images have higher resolution than possible')
        if img.height > max_height or img.width > max_width:
            raise MaxResolutionErrorException('Your images have smallest resolution than possible')
        super().save(*args, **kwargs)



class Notebook(Product):

    diagonal = models.CharField(max_length=255, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name='Type of display')
    processor_freq = models.CharField(max_length=255, verbose_name='Processor')
    ram = models.CharField(max_length=255, verbose_name='OP')
    time_without_charge = models.CharField(max_length=255, verbose_name='Time battery')

    def __str__(self):
        return "{0} : {1}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='Diagonal')
    display_type = models.CharField(max_length=255, verbose_name='Type of display')
    resolution = models.CharField(max_length=255, verbose_name='Pix of display')
    accum_volume = models.CharField(max_length=255, verbose_name='Battery')
    ram = models.CharField(max_length=255, verbose_name='OP')
    sd = models.BooleanField(default=True, verbose_name='SD card')
    sd_volume_max = models.CharField(max_length=255, null=True, blank=True, verbose_name='Max OP')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Main Camera')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Front Camera')

    def __str__(self):
        return "{0} : {1}".format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')

    # @property
    # def sd(self):
    #     if self.sd:
    #         return 'Yes'
    #     return 'No'








class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='customer', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='carts', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Final Price')

    def __str__(self):
        return "Product {0} (for busket)".format(self.content_object.title)


class Cart(models.Model):
    owner = models.ForeignKey('Customer', verbose_name='Owner', on_delete=models.CASCADE )
    products = models.ManyToManyField(CartProduct, related_name='carts', blank=True)
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Final Price')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Phone Number')
    address = models.CharField(max_length=255, verbose_name='Address')

    def __str__(self):
        return "Customer: {0} {1}".format(self.user.first_name, self.user.last_name)


