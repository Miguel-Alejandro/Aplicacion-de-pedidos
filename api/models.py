from django.db import models

class hoyRX(models.Model):

    email = models.CharField(max_length=100)
    sendCheckoutByEmail = models.BooleanField(default=True)
    address = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    Zip = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return '{0}, {1}'.format(self.name, self.last_name)




class item(models.Model):
    code = models.IntegerField()
    quantity = models.IntegerField()
    date = models.DateField(blank=False, null=False)
    name = models.ForeignKey(hoyRX, on_delete=models.CASCADE)
    