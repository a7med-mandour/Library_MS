from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Book(models.Model):

    book_status= [

        ('available','available'),
        ('rental','rental'),
        ('sold','sold'),
            ]

    title= models.CharField(max_length=200)
    author = models.CharField(max_length=100, null=True, blank=True)
    book_photo = models.ImageField(upload_to="photo", null=True, blank=True)
    author_image= models.ImageField(upload_to="photo", null=True, blank=True)
    pages = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=5,decimal_places=2 , null=True,blank=True)
    rental_price_day = models.DecimalField(max_digits=5,decimal_places=2 , null=True,blank=True)
    rental_period = models.IntegerField(null=True,blank=True)
    activity = models.BooleanField(default=True)
    status = models.CharField(max_length=50, choices=book_status, null=True, blank=True)
    category = models.ForeignKey(Category,on_delete= models.PROTECT, blank=True,null=True)


    def clean(self):
        # if not self.price and not self.rental_price_day:
        #     raise ValidationError('At least one of field_a or field_b must be filled.')
        if self.price and self.rental_price_day:
            raise ValidationError('Only one of price or rental price day can be filled.')


    def __str__(self) -> str:
        return self.title
