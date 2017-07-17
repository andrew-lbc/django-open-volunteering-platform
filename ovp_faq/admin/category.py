from django.contrib import admin
from django import forms

from ovp_faq.models import Category

class CategoryAdmin(admin.ModelAdmin):
	list_display = ['id', 'name']


admin.site.register(Category, CategoryAdmin)