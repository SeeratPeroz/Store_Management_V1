from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path("", views.welcome_Page),
    path("Home/", views.HOME,name='HOME'),
    path("Home/Add_Product", views.add_Product, name="Add_Product"),
    path("Home/add_Category", views.add_Category, name="add_Category"),
   # path("Home/borrower", views.Borrower_List, name="Borrower_List"),
    path("Home/Record_Purchase", views.Record_Purchase, name="Record_Purchase"),
    path("Home/Supplier", views.AddSupplier, name="Add_Supplier"),
    path("Home/AddPuchase", views.AddPuchase, name="AddPuchase"),
    path("Home/Stock", views.AddStock, name="Stock"),
    path("Home/search_product", views.search_product, name="search_product"),
    path("Home/Update_product", views.Update_product, name="Update_product"),
    path("Home/Chaier_Details", views.Chaier_Details, name="Chaier_Details"),
    path("Home/Remove_Cashier", views.Remove_Cashier, name="Remove_Cashier"),
    path("Home/Invoice_Summary", views.Invoice_Summary, name="Invoice_Summary"),
    path("Home/Stock_Summary", views.Stock_Summary, name="Stock_Summary"),
    path("Home/Purchase_Summary", views.Purchase_Summary, name="Purchase_Summary"),
    path("Home/PieChart", views.PieChart, name="PieChart"),
    path("Home/OnStock", views.OnStock, name="OnStock"),
    path("Home/cancelPurchase", views.cancelPurchase, name="cancelPurchase"),
    path("Home/Create_Invoice", views.Create_Invoice, name="Create_Invoice"),
    path("Home/Invoice", views.Invoice, name="Invoice"),
    path("Home/add_Customer", views.add_Customer, name="add_Customer"),
    path("Home/ShowINVsummary", views.ShowINVsummary, name="ShowINVsummary"),
    path("Home/ShowPURsummary", views.ShowPURsummary, name="ShowPURsummary"),
    path("Home/ExportOnstock", views.ExportOnstock, name="ExportOnstock"),
    path("Home/ExportStkSummary", views.ExportStkSummary, name="ExportStkSummary"),
    re_path(r"^Home/RemovePurch/(?P<itmID>[0-9]+)/(?P<purNO>[0-9]+)$", views.RemovePurch_View, name="RemovePurch"),
    re_path(r"^Home/RemoveINV/(?P<itmID>[0-9]+)s/(?P<invNO>[0-9]+)$", views.RemoveINV_View, name="RemoveINV"),

]
