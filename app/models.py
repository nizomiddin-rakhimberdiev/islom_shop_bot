from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.TextField()  # agar rasm URL bo‘lsa
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class User(models.Model):
    user_id = models.CharField(max_length=20)
    locale = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id


class Cart(models.Model):
    user_id = models.CharField(max_length=20)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    total_price = models.IntegerField()

    def __str__(self):
        return f"{self.user_id} - {self.product.name}"



class Order(models.Model):
    user_id = models.CharField(max_length=20)  # SQLite dagi kabi simple text
    products = models.TextField()  # JSON yoki matn bo‘lishi mumkin
    phone = models.CharField(max_length=50)
    lokation = models.TextField()
    tolov_turi = models.CharField(max_length=100)
    sana = models.CharField(max_length=100)  # yoki DateTimeField ham bo‘ladi

    def __str__(self):
        return f"Order {self.id} - {self.user}"
