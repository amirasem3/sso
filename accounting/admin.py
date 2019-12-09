from django.contrib import admin

from django.apps import apps

from panel.models import ConsumerSiteAllowedField
from .models import *

app = apps.get_app_config('accounting')

for model_name, model in app.models.items():
    admin.site.register(model)


class ConsumerSite_InLine(admin.TabularInline):
    model = ConsumerSite.owners.through
    verbose_name_plural = 'providing Sites'


class DesiredBigIntField_InLine(admin.TabularInline):
    model = DesiredIntegerField


class DesiredBool_InLine(admin.TabularInline):
    model = DesiredBooleanField


class DesiredCharField_InLine(admin.TabularInline):
    model = DesiredCharField


class DesiredEmailField_InLine(admin.TabularInline):
    model = DesiredEmailField


class DesiredImageField_InLine(admin.TabularInline):
    model = DesiredImageField


class DesiredTextField_InLine(admin.TabularInline):
    model = DesiredTextField


class PF(admin.ModelAdmin):
    inlines = [
        ConsumerSite_InLine,
        DesiredBigIntField_InLine,
        DesiredCharField_InLine,
        DesiredBool_InLine,
        DesiredTextField_InLine,
        DesiredImageField_InLine,
        DesiredEmailField_InLine
    ]


class ConsumerSiteAllowedField_InLine(admin.TabularInline):
    model = ConsumerSiteAllowedField
    verbose_name_plural = 'Allowed Fields'


class CS(admin.ModelAdmin):
    inlines = [
        ConsumerSiteAllowedField_InLine
    ]


admin.site.unregister(Profile)
admin.site.register(Profile, PF)
admin.site.unregister(ConsumerSite)
admin.site.register(ConsumerSite, CS)
