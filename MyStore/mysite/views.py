from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
import cv2
from pyzbar import pyzbar
from .models import *
from django.db.models import Sum
import winsound
from accounts.models import User
from django.db import connection
from django.contrib import auth
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa


def welcome_Page(request):
    return render(request, "Lets_Start.html", {})


@login_required
def HOME(request):
    c = request.user
    x=c
    f = open('put.txt','w')
    f.write('0')
    f.close()
    ff = open('invN.txt','w')
    ff.write('0')
    ff.close()
    return render(request, "king.html", {'c':c})


@login_required
def add_Product(request):
    x = str
    if request.method == 'POST':
        pCode = request.POST['Pcode']
        pName = request.POST['Pname']
        Unit_M = request.POST['UnM']
        Desc = request.POST['desc']
        x = request.POST.get("dropdown")
        cn = Category()
        cn.catID = x
        if Item.objects.filter(itmID=pCode).exists():
            messages.info(request, "Product code is already used.")
            return redirect("Add_Product")
        else:
            addPrd = Item.objects.create(itmID=pCode, unitMeaure=Unit_M, catID=cn, itmName=pName, Desc=Desc)
            addPrd.save();
            messages.info(request, "Product added.")
            return redirect("Add_Product")
    else:
        frequency = 2500  # Set Frequency To 2500 Hertz
        duration = 1000  # Set Duration To 1000 ms == 1 second

        camera = cv2.VideoCapture(1)
        ret, frame = camera.read()
        while ret:
            ret, frame = camera.read()
            # frame = read_barcodes(frame)
            barcodes = pyzbar.decode(frame)
            for barcode in barcodes:
                x, y, w, h = barcode.rect
                barcode_text = barcode.data.decode('utf-8')
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                winsound.Beep(frequency, duration)
                ret = False
                x = barcode_text
                break

            cv2.imshow('Barcode reader', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

        camera.release()
        cv2.destroyAllWindows()
        catDetails = Category.objects.all()
        return render(request, 'add_product.html', {'cat': catDetails, 'xc':x})


@login_required
def add_Category(request):
    if request.method == 'POST':
        caName = request.POST['catName']
        if Category.objects.filter(catName=caName).exists():
            messages.info(request, caName + " is already added to the list.")
            return redirect("add_Category")
        else:
            myCat = Category.objects.create(catName=caName)
            myCat.save();
            messages.info(request, caName + " is Added to the list.")
            return redirect("add_Category")
    else:
        return render(request, 'addcat.html', {})


# This function is use for next version
"""
@login_required
def Borrower_List(request):
    bor = SalesDetails.objects.all().filter(paid='NOT')
    
    return render(request, 'borrower.html', {'bor': bor})
"""

@login_required
def AddSupplier(request):
    if request.method == 'POST':
        SupName = request.POST['spName']
        SupPhone = request.POST['spPhone']
        SupAdd = request.POST['spAdd']
        if Supplier.objects.filter(supName=SupName).exists():
            messages.info(request, SupName + " is already taken.")
            return redirect('Add_Supplier')
        else:
            mySup = Supplier.objects.create(supName=SupName, supPhone=SupPhone, supAdd=SupAdd)
            mySup.save();
            messages.info(request, "Supplier is added to the list.")
            return redirect('Add_Supplier')
    else:
        return render(request, 'supplier.html', {})


@login_required
def AddPuchase(request):
    if request.method == "POST":
        SupName = request.POST.get('dropdown')
        PurDate = request.POST['purDate']
        spDetails = Supplier()
        spDetails.supID = SupName
        if PurDate == '':
            mypur = Purchase.objects.create(supID=spDetails)
            messages.info(request, "Purchase has been recorded")
            return redirect("AddPuchase")
        else:
            mypur = Purchase.objects.create(purDate=PurDate, supID=spDetails)
            messages.info(request, "Purchase has been recorded")
            return redirect("AddPuchase")
    else:
        sup = Supplier.objects.all()
        return render(request, 'purchase.html', {'sup': sup})



@login_required
def AddStock(request):
    try:
        if request.method == 'POST':
            stk = request.POST['sktName']
            if Stock.objects.filter(stkName=stk).exists():
                messages.info(request, "Stock already exists.")
                return redirect('Stock')
            else:
                addStk = Stock.objects.create(stkName=stk)
                addStk.save()
                messages.info(request, stk + " is added to the list.")
                return redirect('Stock')
            return redirect('Stock')
        else:
            return render(request, 'Stock.html', {})

    except Exception as ex:
        messages.info(request,ex)
        return redirect('AddStock')
@login_required
def search_product(request):
    try:
        x = str
        if request.method == 'POST':
            pNam = request.POST['sField']
            if pNam != '':
                if Item.objects.filter(itmID=pNam).exists():
                    empDetails = Item.objects.all().filter(itmID=pNam)
                    cat = Category.objects.all()
                    return render(request, 'Update_product.html', {'stf': empDetails, 'cat': cat})
                else:
                    messages.info(request, 'Product not found.')
                    return redirect('search_product')
            else:
                messages.info(request, 'Product not found.')
                return redirect('search_product')
        else:
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second

            camera = cv2.VideoCapture(1)
            ret, frame = camera.read()
            while ret:
                ret, frame = camera.read()
                # frame = read_barcodes(frame)
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    x, y, w, h = barcode.rect
                    barcode_text = barcode.data.decode('utf-8')
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    winsound.Beep(frequency, duration)
                    ret = False
                    x = barcode_text
                    break
                cv2.imshow('Barcode reader', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            camera.release()
            cv2.destroyAllWindows()
            return render(request, 'Update_product.html', {'xc':x})
    except Exception as ex:
        messages.info(request,ex)
        return redirect(reverse('search_product'))

@login_required
def Update_product(request):
    try:
        if request.method == 'POST':
            prdCode = request.POST['prdCode']
            prdCodee = request.POST['prdCode']
            prdName = request.POST['prdName']
            prdUnit = request.POST['prdUnit']
            x = request.POST.get("dropdown")
            cn = Category()
            cn.catID = x
            prdCOom = request.POST['prdComment']
            upd = Item.objects.select_related().filter(itmID=prdCode).update(itmID=prdCodee, itmName=prdName,
                                                                             unitMeaure=prdUnit, catID=cn, Desc=prdCOom)
            messages.info(request, 'Changes successfully made.')
            return redirect('search_product')
        else:
            return render(request, 'Update_product.html', {})
    except Exception as ex:
        messages.info(request,ex)
        return redirect('Update_product')

@login_required
def Invoice_Summary(request):
    try:
        if request.method == "POST":
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            p = SalesInv.objects.raw(
                "SELECT mysite_salesinv.invNO, mysite_salesinv.Salse_Date, mysite_salesinv.cusID_id, sum(mysite_salesdetails.TotalSale) as tot FROM mysite_salesinv  INNER JOIN mysite_salesdetails ON mysite_salesinv.invNO = mysite_salesdetails.invNO_id WHERE mysite_salesinv.Salse_Date between '%s' and '%s' GROUP BY mysite_salesinv.invNO;" % (
                    start_date, end_date))
            # print(p.query)
            return render(request, 'inovice_Summary.html', {'pubs2': p})
        else:
            p = SalesInv.objects.raw("""
                                        SELECT mysite_salesinv.invNO, 
                                        mysite_salesinv.Salse_Date,
                                        mysite_salesinv.cusID_id,
                                        sum(mysite_salesdetails.TotalSale) as tot
                                        FROM mysite_salesinv
                                        INNER JOIN
                                        mysite_salesdetails ON mysite_salesinv.invNO = mysite_salesdetails.invNO_id
                                        GROUP BY mysite_salesinv.invNO;
            """)
            return render(request, 'inovice_Summary.html', {'pubs2': p})
    except Exception as ex:
        messages.info(request,ex)
        return redirect('Invoice_Summary')

@login_required
def Remove_Cashier(request):
    if request.method == "POST":
        pass
    else:
        cashD = User.objects.all()
        return render(request, 'Remove_cashier.html', {})


@login_required
def Chaier_Details(request):
    try:
        if request.method == "POST":
            redirect('Chaier_Details')
        else:
            cashD = User.objects.all().filter(is_admin=False)
            return render(request, 'cashier_details.html', {'cash': cashD})
    except Exception as ex:
        messages.info(request,ex)
        return redirect('Chaier_Details')

@login_required
def Record_Purchase(request):
    try:
        xl = str
        if request.method == 'POST':
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second

            camera = cv2.VideoCapture(1)
            ret, frame = camera.read()
            while ret:
                ret, frame = camera.read()
                # frame = read_barcodes(frame)
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    x, y, w, h = barcode.rect
                    barcode_text = barcode.data.decode('utf-8')
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    winsound.Beep(frequency, duration)
                    ret = False
                    xl = barcode_text
                    break
                cv2.imshow('Barcode reader', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            camera.release()
            cv2.destroyAllWindows()

            purCH = request.POST.get('dropdown')
            prdNO = request.POST['productNO']
            stkName = request.POST.get('dropdown2')

            PrdQTY = request.POST['prdQty']
            UnitCost = request.POST['unitCost']
            Comment = request.POST['comment']
            sRate = request.POST['saleRate']

            file = open('put.txt','w')
            file.write(purCH)
            file.close()
            if PurchaseDetails.objects.filter(itmID=prdNO, purNO=purCH).exists():
                messages.info(request, "Product already added to the list.")

                file = open('put.txt', 'r')
                mypurch = file.read()
                file.close()
                purDetails = PurchaseDetails.objects.select_related('itmID').filter(purNO=mypurch)
                Purc = Purchase.objects.all()
                stkDetails = Stock.objects.all()
                return render(request, 'record_purchase.html',
                              {'sup': Purc, 'sup1': stkDetails, 'sup2': purDetails, 'xc': xl})
            else:
                prdD = PurchaseDetails()
                x = Item()
                x.itmID = prdNO
                prdD.itmID = x

                PURCH = Purchase()
                PURCH.purNO = purCH
                prdD.purNO = PURCH

                STK = Stock()
                STK.stkID = stkName
                prdD.sktID = STK

                prdD.purQty = PrdQTY
                prdD.UnitCost = UnitCost
                prdD.Comment = Comment
                prdD.ssRate = sRate
                cal = int(PrdQTY) * int(UnitCost)
                prdD.purTotal = cal
                prdD.save()
                PurchaseDetails.objects.filter(itmID=prdNO).update(ssRate=sRate)
                purDetails = PurchaseDetails.objects.select_related('itmID').filter(purNO=PURCH)
                Purc = Purchase.objects.all()
                stkDetails = Stock.objects.all()
                return render(request, 'record_purchase.html', {'sup': Purc, 'sup1': stkDetails, 'sup2': purDetails,'xc':xl})
        else:
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second

            camera = cv2.VideoCapture(1)
            ret, frame = camera.read()
            while ret:
                ret, frame = camera.read()
                # frame = read_barcodes(frame)
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    x, y, w, h = barcode.rect
                    barcode_text = barcode.data.decode('utf-8')
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    winsound.Beep(frequency, duration)
                    ret = False
                    xl = barcode_text
                    break
                cv2.imshow('Barcode reader', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            camera.release()
            cv2.destroyAllWindows()
            file = open('put.txt','r')
            mypurch= file.read()
            if mypurch=='':
                mypurch='0'
            file.close()
            purDetails = PurchaseDetails.objects.select_related('itmID').filter(purNO=mypurch)
            Purc = Purchase.objects.all()
            stkDetails = Stock.objects.all()
            return render(request, 'record_purchase.html', {'sup': Purc, 'sup1': stkDetails, 'sup2': purDetails, 'xc': xl})
    except Exception as ex:
        messages.info(request,ex)
        return redirect(reverse('Record_Purchase'))

@login_required
def cancelPurchase(request):
    if request.method == 'POST':
        purCH = request.POST.get('dropdown')
        print(purCH)
        return render(request, 'record_purchase.html', {})
    else:
        return render(request, "king.html", {})


@login_required
def Stock_Summary(request):
    try:
        if request.method == 'POST':
            pass
        else:
            with connection.cursor() as cursor2:
                cursor2.execute("""
    SELECT Total_Purch.itmID_id,
           Total_Purch.itmName,
           Total_Purch.unitMeaure,
           Total_Purch.stkName,
           (Total_Purch.TSQN - IfNULL(Total_Sale.TSQO, 0) ) AS StockQty,
           Total_Purch.TSQN,
           ifnull(Total_Purch.PurchRate, 0) as PurchRate,
           ifnull(Total_Sale.TSQO, 0) as TSQO,
           ifNULL(Total_Sale.SalRate, 0)as SalVALUE
      FROM Total_Purch
           LEFT JOIN
           Total_Sale ON Total_Purch.itmID_id = Total_Sale.itmID_id
            """)
                row = cursor2.fetchall()
            return render(request, 'Stock Summary.html', {'row': row})
    except Exception as ex:
        messages.info(request,ex)
        return redirect('Stock_Summary')

@login_required
def Purchase_Summary(request):
    try:
        if request.method == "POST":
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            p = Purchase.objects.raw("""
                                        SELECT mysite_purchase.purNO,
                                        mysite_purchase.purDate,
                                        mysite_purchase.supID_id,
                                        sum(mysite_purchasedetails.purTotal) as tot
                                    FROM mysite_purchase
                                        INNER JOIN
                                    mysite_purchasedetails ON mysite_purchasedetails.purNO_id = mysite_purchase.purNO
                                    WHERE mysite_purchase.purDate BETWEEN '%s' AND '%s'
                                    GROUP BY mysite_purchase.purNO;
                                      """ % (start_date, end_date))
            return render(request, 'Purchase_Summary.html', {'pubs2': p})
        else:
            p = Purchase.objects.raw("""
                                        SELECT mysite_purchase.purNO,
                                         mysite_purchase.purDate,
                                        mysite_purchase.supID_id,
                                        sum(mysite_purchasedetails.purTotal) AS tot
                                        FROM mysite_purchase
                                        INNER JOIN
                                        mysite_purchasedetails ON mysite_purchasedetails.purNO_id = mysite_purchase.purNO
                                        GROUP BY mysite_purchase.purNO;
    
            """)
            return render(request, 'Purchase_Summary.html', {'pubs2': p})
    except Exception as ex:
        messages.info(request,ex)
        return redirect('Purchase_Summary')

@login_required
def PieChart(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("select sum(TotalSale) as Sale_T from mysite_Salesdetails;")
            row = cursor.fetchone()
        sal = sum(row)

        with connection.cursor() as cursor1:
            cursor1.execute("SELECT sum(purTotal) FROM mysite_purchasedetails")
            row2 = cursor1.fetchone()
        pur = sum(row2)
        context = {'sale': sal, 'purch': pur}
        return render(request, 'PieChart.html', context)
    except Exception as ex:
        messages.info(request,ex)
        return redirect('HOME')

@login_required
def OnStock(request):
    try:
        if request.method == "POST":
            return render(request, 'OnStock.html', {})
        else:
            with connection.cursor() as cursor2:
                cursor2.execute("""
                SELECT Total_Purch.itmID_id,
           Total_Purch.itmName,
           Total_Purch.unitMeaure,
           Total_Purch.stkName,
           (Total_Purch.TSQN - IfNULL(Total_Sale.TSQO, 0) ) AS StockQty
      FROM Total_Purch 
           LEFT JOIN
           Total_Sale ON Total_Purch.itmID_id = Total_Sale.itmID_id
    """)
                row = cursor2.fetchall()
            return render(request, 'OnStock.html', {'row':row})
    except Exception as ex:
        messages.info(request,ex)
        return redirect('OnStock')

@login_required
def Invoice(request):
    try:
        if request.method == "POST":
            CusName = request.POST.get('dropdown')
            PurDate = request.POST['purDate']
            cuDetails = Customer()
            cuDetails.cusID = CusName
            if PurDate == '':
                mypur = SalesInv.objects.create(cusID=cuDetails)
                messages.info(request, "Invoice has been recorded")
                return redirect("Invoice")
            else:
                mypur = SalesInv.objects.create(Salse_Date=PurDate, cusID=cuDetails)
                messages.info(request, "Invoice has been recorded")
                return redirect("Invoice")
        else:
            CUS = Customer.objects.all()
            return render(request, 'Invoice.html', {'sup': CUS})
    except Exception as ex:
        messages.info(request,ex)
        return redirect('Invoice')


@login_required
def add_Customer(request):
    try:
        if request.method == 'POST':
            CusName = request.POST['spName']
            CusPhone = request.POST['spPhone']
            CusAdd = request.POST['spAdd']
            if Customer.objects.filter(cusName=CusName).exists():
                messages.info(request, CusName + " is already taken.")
                return redirect('add_Customer')
            else:
                mySup = Customer.objects.create(cusName=CusName, cusPhone=CusPhone, cusAdd=CusAdd)
                mySup.save();
                messages.info(request, "Customer is added to the list.")
                return redirect('add_Customer')
        else:
            return render(request, 'Customer.html', {})
    except Exception as ex:
        return redirect('add_Customer')

# Function to create new Invoices
@login_required
def Create_Invoice(request):
    try:
        xl = ''
        if request.method == 'POST':

            purCH = request.POST.get('dropdown')
            prdNO = request.POST['productNO']
            PrdQTY = request.POST['prdQty']
            stkName = request.POST.get('dropdown2')
            UnitCost = request.POST['unitCost']
            Discount = request.POST['dicount']
            ExtraCH = request.POST['extraCH']
            Paid = request.POST.get('paid')
            fnx = open('invN.txt','w')
            fnx.write(purCH)
            fnx.close()
            # Camera will start agian
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second

            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second

            camera = cv2.VideoCapture(1)
            ret, frame = camera.read()
            while ret:
                ret, frame = camera.read()
                # frame = read_barcodes(frame)
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    x, y, w, h = barcode.rect
                    barcode_text = barcode.data.decode('utf-8')
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    winsound.Beep(frequency, duration)
                    ret = False
                    xl = barcode_text
                    break
                cv2.imshow('Barcode reader', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            # TO get Sale Rate
            if xl == '':
                xl='0'
            Rate = PurchaseDetails.objects.raw('SELECT * FROM mysite_purchasedetails WHERE itmID_id = %s group by itmID_id' %(xl))
            # to show Sales Rate


            camera.release()
            cv2.destroyAllWindows()


            if Paid == None:
                Paid = "PAID"
            else:
                pass
            if SalesDetails.objects.filter(itmID=prdNO, invNO=purCH).exists():
                messages.info(request, "Product already added to the list.")
                purDetails = SalesInv.objects.all()
                stkDetails = Stock.objects.all()
                ppurDetails = SalesDetails.objects.select_related('itmID').filter(invNO=purCH)
                with connection.cursor() as cursor:
                    cursor.execute("select sum(exactCost) as Sale_T from mysite_Salesdetails where invNO_id= " + purCH)
                    row = cursor.fetchone()
                sumTotal = sum(row)
                with connection.cursor() as cursor1:
                    cursor1.execute("select sum(sumDiscount) as Sale_T from mysite_Salesdetails where invNO_id= " + purCH)
                    row = cursor1.fetchone()
                    cursor1.close()
                sumDiscount = sum(row)
                with connection.cursor() as cursor2:
                    cursor2.execute("select sum(TotalSale) as Sale_T from mysite_Salesdetails where invNO_id= " + purCH)
                    row = cursor2.fetchone()
                TOTAL = sum(row)
                return render(request, 'Create_Invoice.html',
                              {'sup': purDetails, 'sup1': stkDetails, 'sup2': ppurDetails,
                               'sumTotal': sumTotal, 'sumDiscount': sumDiscount, 'TOTAL': TOTAL, 'xc':xl,'srate':Rate})
            else:
                prdD = SalesDetails()
                x = Item()
                x.itmID = prdNO
                prdD.itmID = x

                PURCH = SalesInv()
                PURCH.invNO = purCH
                prdD.invNO = PURCH

                STK = Stock()
                STK.stkID = stkName
                prdD.stkID = STK

                prdD.Qty = PrdQTY
                prdD.sRate = UnitCost
                dsc = int(Discount)
                ext = int(ExtraCH)
                cal = int(PrdQTY) * int(UnitCost)
                prdD.exactCost = cal
                prdD.sumDiscount = dsc
                MyCost = cal - dsc
                MyCost = MyCost + ext
                prdD.TotalSale = MyCost
                prdD.paid = Paid
                prdD.EXtraSale = ext
                prdD.save()
                purDetails = SalesDetails.objects.select_related('itmID').filter(invNO=PURCH)
                Purc = SalesInv.objects.all()
                stkDetails = Stock.objects.all()
                with connection.cursor() as cursor:
                    cursor.execute("select sum(exactCost) as Sale_T from mysite_Salesdetails where invNO_id= " + purCH)
                    row = cursor.fetchone()
                sumTotal = sum(row)
                with connection.cursor() as cursor1:
                    cursor1.execute("select sum(sumDiscount) as Sale_T from mysite_Salesdetails where invNO_id= " + purCH)
                    row = cursor1.fetchone()
                    cursor1.close()
                sumDiscount = sum(row)
                with connection.cursor() as cursor2:
                    cursor2.execute("select sum(TotalSale) as Sale_T from mysite_Salesdetails where invNO_id= " + purCH)
                    row = cursor2.fetchone()
                TOTAL = sum(row)


            return render(request, 'Create_Invoice.html',
                          {'sup': Purc, 'sup1': stkDetails, 'sup2': purDetails, 'discount': Discount, 'extra': ExtraCH,
                           'sumTotal': sumTotal, 'sumDiscount': sumDiscount, 'TOTAL': TOTAL,'xc':xl,'srate':Rate})
        else:
            xl = ''
            frequency = 2500  # Set Frequency To 2500 Hertz
            duration = 1000  # Set Duration To 1000 ms == 1 second

            camera = cv2.VideoCapture(1)
            ret, frame = camera.read()
            while ret:
                ret, frame = camera.read()
                # frame = read_barcodes(frame)
                barcodes = pyzbar.decode(frame)
                for barcode in barcodes:
                    x, y, w, h = barcode.rect
                    barcode_text = barcode.data.decode('utf-8')
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    winsound.Beep(frequency, duration)
                    ret = False
                    xl = barcode_text
                    break
                cv2.imshow('Barcode reader', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    break

            camera.release()
            cv2.destroyAllWindows()



            # TO get Sale Rate
            if xl == '':
                xl='0'
            Rate = PurchaseDetails.objects.raw('SELECT * FROM mysite_purchasedetails WHERE itmID_id = %s group by itmID_id' %(xl))


            purDetails = SalesInv.objects.all()
            stkDetails = Stock.objects.all()
            myinv = open('invN.txt','r')
            mINV = myinv.read()
            if mINV == '':
                mINV='0'
            myinv.close()

            ppurDetails = SalesDetails.objects.select_related('itmID').filter(invNO=mINV)
            with connection.cursor() as cursor:
                cursor.execute("select ifnull(sum(exactCost),0) as Sale_T from mysite_Salesdetails where invNO_id= " + mINV)
                row = cursor.fetchone()
            sumTotal = sum(row)
            with connection.cursor() as cursor1:
                cursor1.execute("select ifnull(sum(sumDiscount),0) as Sale_T from mysite_Salesdetails where invNO_id= " + mINV)
                row = cursor1.fetchone()
                cursor1.close()
            sumDiscount = sum(row)
            with connection.cursor() as cursor2:
                cursor2.execute("select ifnull(sum(TotalSale),0) as Sale_T from mysite_Salesdetails where invNO_id= " + mINV)
                row = cursor2.fetchone()
            TOTAL = sum(row)
            return render(request, 'Create_Invoice.html',
                          {'sup': purDetails, 'sup1': stkDetails, 'sup2': ppurDetails,
                           'sumTotal': sumTotal, 'sumDiscount': sumDiscount, 'TOTAL': TOTAL, 'xc':xl, 'srate':Rate})

    except Exception as ex:
        messages.info(request,ex)
        return  redirect(reverse('HOME'))
@login_required
def ShowINVsummary(request):
    start_date = request.GET.get('start_date')
    # end_date = request.POST.get('end_date')
    print("Date: ", start_date)
    Invoice = SalesInv.objects.raw(
        "SELECT mysite_salesinv.invNO, mysite_salesinv.Salse_Date, mysite_salesinv.cusID_id, sum(mysite_salesdetails.TotalSale) as tot FROM mysite_salesinv  INNER JOIN mysite_salesdetails ON mysite_salesinv.invNO = mysite_salesdetails.invNO_id group by mysite_salesinv.invNO;")
    template_path = 'InvReport.html'
    context = {'Invoice': Invoice}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Invoice_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# Function to export the Purchase Summary.
@login_required
def ShowPURsummary(request):
    start_date = request.GET.get('start_date')
    # end_date = request.POST.get('end_date')
    print("Date: ", start_date)
    PURCHASE_SUM = Purchase.objects.raw(
        "SELECT mysite_purchase.purNO, mysite_purchase.purDate, mysite_purchase.supID_id, sum(mysite_purchasedetails.purTotal) as tot FROM mysite_purchase INNER JOIN mysite_purchasedetails ON mysite_purchasedetails.purNO_id = mysite_purchase.purNO GROUP BY mysite_purchase.purNO;")
    template_path = 'PurReport.html'
    context = {'PURCHASE_SUM': PURCHASE_SUM}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Purchase_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


@login_required
def RemovePurch_View(request, **kwargs):
    delPurDet = PurchaseDetails.objects.filter(itmID=kwargs.get('itmID'), purNO=kwargs.get('purNO'))
    delPurDet.delete()
    return redirect('Record_Purchase')

@login_required
def RemoveINV_View(request, **kwargs):
    delPurDet = SalesDetails.objects.filter(itmID=kwargs.get('itmID'), invNO=kwargs.get('invNO'))
    delPurDet.delete()
    return redirect('Create_Invoice')

# Function to export OnStock Details
@login_required
def ExportOnstock(request):
    with connection.cursor() as cursor2:
        cursor2.execute("""
                SELECT Total_Purch.itmID_id,
           Total_Purch.itmName,
           Total_Purch.unitMeaure,
           Total_Purch.stkName,
           (Total_Purch.TSQN - IfNULL(Total_Sale.TSQO, 0) ) AS StockQty
      FROM Total_Purch
           LEFT JOIN
           Total_Sale ON Total_Purch.itmID_id = Total_Sale.itmID_id
    """)
        row = cursor2.fetchall()
    template_path = 'OnStkReport.html'
    context = {'row': row}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="OnStock_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


# Function to Export Stock Summary
@login_required
def ExportStkSummary(request):
    with connection.cursor() as cursor2:
        cursor2.execute("""
        SELECT Total_Purch.itmID_id,
               Total_Purch.itmName,
               Total_Purch.unitMeaure,
               Total_Purch.stkName,
               (Total_Purch.TSQN - IfNULL(Total_Sale.TSQO, 0) ) AS StockQty,
               Total_Purch.TSQN,
               ifnull(Total_Purch.PurchRate, 0) as PurchRate,
               ifnull(Total_Sale.TSQO, 0) as TSQO,
               ifNULL(Total_Sale.SalRate, 0)as SalVALUE
          FROM Total_Purch
               LEFT JOIN
               Total_Sale ON Total_Purch.itmID_id = Total_Sale.itmID_id
                """)
        row = cursor2.fetchall()
    template_path = 'StkSummaryReport.html'
    context = {'row': row}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="StockSummary_report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
