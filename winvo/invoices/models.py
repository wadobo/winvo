from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    name = models.CharField(max_length=10)
    cif = models.CharField(max_length=63)
    address = models.CharField(max_length=255)


class Project(models.Model):
    company = models.ForeignKey(Company)
    name = models.CharField(max_length=255)
    currency = models.CharField(max_length=255)
    tax = models.FloatField(default=21.0)
    taxname = models.CharField(max_length=31, default='IVA (21%)')

    dateformat = models.CharField(max_length=31, default='%d de %B de %Y')
    expirydate = models.PositiveSmallIntegerField(default=30)


class Invoice(models.Model):
    project = models.ForeignKey(Project, null=True)
    year = models.PositiveSmallIntegerField()
    num = models.PositiveIntegerField(editable=False)
    date = models.DateField(auto_now_add=True, default=now())

    def _next_num(self):
        # increment invoice num
        last_invoice = Invoice.objects.filter(year=self.year).order_by('num').last()
        if not last_invoice:
            num = 1
        else:
            num = last_invoice.num + 1
        return num

    def save(self, *args, **kwargs):
        self.num = self._next_num()
        super(Invoice, self).save(*args, **kwargs)


class Fee(models.Model):
    invoice = models.ForeignKey(Invoice)
    summary = models.CharField(max_length=1023)
    fee = models.FloatField(default=35.0)
    hours = models.FloatField(blank=True, null=True)


CONFIG_TYPE = (
        ('total', 'total'),
        ('hours', 'hours'),
)
LANG = (
        ('es', 'es'),
        ('en', 'en'),
)
class Config(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    payment = models.CharField(max_length=255)
    ctype = models.CharField(max_length=5, choices=CONFIG_TYPE, default="hours")
    lang = models.CharField(max_length=2, choices=LANG, default="es")
    locale = models.CharField(max_length=31)
