from django.db import models

class Branch(models.Model):
    branch_name = models.CharField(max_length=70, default='',
                            verbose_name='Branch')
    code = models.CharField(max_length=15,default='',
                            verbose_name='Branch Code', primary_key=True)   
    description = models.TextField(max_length=500,
                            default='',
                            verbose_name='Description',
                            blank=True)
