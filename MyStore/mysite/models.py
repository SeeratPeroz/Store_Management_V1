from django.db import models
from accounts.models import User


# Create your models here.

class Category(models.Model):
    catID = models.AutoField(primary_key=True)
    catName = models.CharField(max_length=45, unique=True)

    def __str__ (self):
        return self.catName


class Item(models.Model):
    itmID = models.IntegerField(primary_key=True, unique=True)
    itmName = models.CharField(max_length=45)
    unitMeaure = models.CharField(max_length=10)
    catID = models.ForeignKey(Category, on_delete=models.SET_NULL,null=True,  blank=True)
    Desc = models.CharField(max_length=150)

    def __str__(self):
        return self.itmName


class Expences(models.Model):
    expID = models.AutoField(primary_key=True)
    expName = models.CharField(max_length=45)

    def __str__(self):
        return self.expName


class CashPoint(models.Model):
    cpID = models.AutoField(primary_key=True)
    cpName = models.CharField(max_length=45)

    def __str__(self):
        return self.cpName


class ExpencedDetails(models.Model):
    expID = models.ForeignKey(Expences, on_delete=models.SET_NULL, null=True,  blank=True)
    amPaid = models.IntegerField()
    expnDate = models.DateTimeField(auto_now_add=True)  # auto_now_add=True is added to automatically add the date.
    cpID = models.ForeignKey(CashPoint, on_delete=models.SET_NULL,null=True,  blank=True)



class Customer(models.Model):
    # I have taken the filed as AutoField becuase i want this field to auto increment
    cusID = models.AutoField(primary_key=True)
    cusName = models.CharField(max_length=45, blank=True)
    cusPhone = models.CharField(max_length=15, blank=True)
    cusAdd = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.cusName



class Stock(models.Model):
    # I have taken the filed as AutoField becuase i want this field to auto increment
    stkID = models.AutoField(primary_key=True)
    stkName = models.CharField(max_length=45)

    def __str__(self):
        return self.stkName

class SalesInv(models.Model):
    # I have taken the filed as AutoField becuase i want this field to auto increment
    invNO = models.AutoField(primary_key=True)
    cusID = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True,  blank=True)
    Salse_Date = models.DateField()  # auto_now_add=True is added to automatically add the date.


class SalesDetails(models.Model):
    itmID = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True,  blank=True)
    Qty = models.IntegerField(default=0)
    invNO = models.ForeignKey(SalesInv, on_delete=models.CASCADE, null=True,  blank=True)
    sRate = models.IntegerField(default=0)
    stkID = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True,  blank=True)
    cpID = models.ForeignKey(CashPoint, on_delete=models.SET_NULL, null=True,  blank=True)
    exactCost = models.IntegerField()
    paid = models.CharField(max_length=10)
    sumDiscount = models.IntegerField()
    EXtraSale = models.IntegerField()
    TotalSale = models.IntegerField(default=0)


# WHo holdes the Stock in which date.
class StockHoldes(models.Model):
    empID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,  blank=True)
    stkH_Date = models.DateTimeField(auto_now_add=True)  # auto_now_add=True is added to automatically add the date.
    stkID = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True,  blank=True)

    def __int__(self):
        return self.empID


# who holdes CashPoint in Which Date.
class CashPointHoldes(models.Model):
    empID = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,  blank=True)
    CPH_Date = models.DateTimeField(auto_now_add=True)  # auto_now_add=True is added to automatically add the date.
    CPID = models.ForeignKey(CashPoint, on_delete=models.SET_NULL, null=True,  blank=True)




class Supplier(models.Model):
    # I have taken the filed as AutoField becuase i want this field to auto increment
    supID = models.AutoField(primary_key=True)
    supName = models.CharField(max_length=45, unique=True)
    supPhone = models.CharField(max_length=15)
    supAdd = models.CharField(max_length=100)

    def __str__(self):
        return self.supName


class Purchase(models.Model):
    # I have taken the filed as AutoField becuase i want this field to auto increment
    purNO = models.AutoField(primary_key=True)
    purDate = models.DateField()
    supID = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True,  blank=True)


class PurchaseDetails(models.Model):
    itmID = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True,  blank=True)
    purNO = models.ForeignKey(Purchase, on_delete=models.CASCADE, null=True,  blank=True)
    sktID = models.ForeignKey(Stock, on_delete=models.SET_NULL, null=True,  blank=True)
    cpID = models.ForeignKey(CashPoint, on_delete=models.SET_NULL, null=True,  blank=True)
    purQty = models.IntegerField(default=0)
    UnitCost = models.IntegerField(default=1)
    purTotal = models.IntegerField()
    Comment = models.TextField()
    ssRate = models.IntegerField(default=0)
