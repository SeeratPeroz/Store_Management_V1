# Generated by Django 3.1.1 on 2020-11-19 10:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CashPoint',
            fields=[
                ('cpID', models.AutoField(primary_key=True, serialize=False)),
                ('cpName', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('catID', models.AutoField(primary_key=True, serialize=False)),
                ('catName', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('cusID', models.AutoField(primary_key=True, serialize=False)),
                ('cusName', models.CharField(blank=True, max_length=45)),
                ('cusPhone', models.CharField(blank=True, max_length=15)),
                ('cusAdd', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Expences',
            fields=[
                ('expID', models.AutoField(primary_key=True, serialize=False)),
                ('expName', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('itmID', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('itmName', models.CharField(max_length=45)),
                ('unitMeaure', models.CharField(max_length=10)),
                ('Desc', models.CharField(max_length=150)),
                ('catID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.category')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('purNO', models.AutoField(primary_key=True, serialize=False)),
                ('purDate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('stkID', models.AutoField(primary_key=True, serialize=False)),
                ('stkName', models.CharField(max_length=45)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('supID', models.AutoField(primary_key=True, serialize=False)),
                ('supName', models.CharField(max_length=45, unique=True)),
                ('supPhone', models.CharField(max_length=15)),
                ('supAdd', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='StockHoldes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stkH_Date', models.DateTimeField(auto_now_add=True)),
                ('empID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('stkID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.stock')),
            ],
        ),
        migrations.CreateModel(
            name='SalesInv',
            fields=[
                ('invNO', models.AutoField(primary_key=True, serialize=False)),
                ('Salse_Date', models.DateField()),
                ('cusID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.customer')),
            ],
        ),
        migrations.CreateModel(
            name='SalesDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Qty', models.IntegerField(default=0)),
                ('sRate', models.IntegerField(default=0)),
                ('exactCost', models.IntegerField()),
                ('paid', models.CharField(max_length=10)),
                ('sumDiscount', models.IntegerField()),
                ('EXtraSale', models.IntegerField()),
                ('TotalSale', models.IntegerField(default=0)),
                ('cpID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.cashpoint')),
                ('invNO', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.salesinv')),
                ('itmID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.item')),
                ('stkID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.stock')),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purQty', models.IntegerField(default=0)),
                ('UnitCost', models.IntegerField(default=1)),
                ('purTotal', models.IntegerField()),
                ('Comment', models.TextField()),
                ('ssRate', models.IntegerField(default=0)),
                ('cpID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.cashpoint')),
                ('itmID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.item')),
                ('purNO', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mysite.purchase')),
                ('sktID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.stock')),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='supID',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.supplier'),
        ),
        migrations.CreateModel(
            name='ExpencedDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amPaid', models.IntegerField()),
                ('expnDate', models.DateTimeField(auto_now_add=True)),
                ('cpID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.cashpoint')),
                ('expID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.expences')),
            ],
        ),
        migrations.CreateModel(
            name='CashPointHoldes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CPH_Date', models.DateTimeField(auto_now_add=True)),
                ('CPID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mysite.cashpoint')),
                ('empID', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]