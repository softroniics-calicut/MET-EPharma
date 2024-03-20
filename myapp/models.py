from django.db import models

# Create your models here.


class Login (models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    statuschoice = (('APPROVED', 'APPROVED'),
              ('PENDING', 'PENDING'),
              ('REJECT', 'REJECT')
              )
    status = models.CharField(choices=statuschoice, max_length=20, default='PENDING',null=True,blank=True)

    type = models.CharField(max_length=10)

    def __str__(self):
        return self.username

class Pharmacy (models.Model):
    name=models.CharField(max_length=20)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)
    email=models.CharField(max_length=20)
    address=models.CharField(max_length=20)
    phone_no=models.IntegerField()
    licence = models.FileField()

    def __str__(self):
        return self.name

class user(models.Model):
    name = models.CharField(max_length=20)
    loginid=models.ForeignKey(Login,on_delete=models.CASCADE)
    address=models.CharField(max_length=20)
    email=models.CharField(max_length=25)
    phone_no=models.IntegerField()

    def __str__(self):
        return self.name                        


class product(models.Model):
    pharmacyid=models.ForeignKey(Pharmacy,on_delete=models.CASCADE)
    image=models.FileField()
    medicinename=models.CharField(max_length=20)
    price=models.IntegerField()
    company=models.CharField(max_length=20)
    type=models.CharField(max_length=10)
    quantity=models.IntegerField()
    prescription_required = models.CharField(max_length=20, default='False') 


    def __str__(self):
        return self.medicinename

class cart(models.Model):
    medicineid=models.ForeignKey(product,on_delete=models.CASCADE)
    userid=models.ForeignKey(user,on_delete=models.CASCADE)
    quantity=models.IntegerField()

    def __str__(self):
        return self.medicineid.medicinename

class Prescription(models.Model):
    file = models.FileField()
    medicine_id = models.ForeignKey(product,on_delete=models.CASCADE)

class booking(models.Model):
    cart_id = models.ForeignKey(cart,on_delete=models.SET_NULL, null=True)
    name=models.ForeignKey(user,on_delete=models.CASCADE)
    medicinename=models.ForeignKey(product,on_delete=models.CASCADE)
    date=models.DateField(auto_now=True,blank=True)
    quantity=models.IntegerField(null=True, blank=True)
    total_amount=models.IntegerField(null=True, blank=True)
    prescription_id = models.ForeignKey(Prescription,on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.medicinename.medicinename


