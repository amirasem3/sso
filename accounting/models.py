from django.contrib.auth.models import User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

field_types = ['DesiredCharField', 'DesiredTextField', 'DesiredIntegerField', 'DesiredBooleanField',
               'DesiredImageField', 'DesiredEmailField']


def get_choices(a):
    return tuple((choice, choice) for choice in a)


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='Profile')
    name = models.CharField(max_length=20, null=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    email = models.EmailField(max_length=70, null=True, unique=True)
    address = models.TextField(max_length=500, null=True)
    gender = models.CharField(max_length=5, null=True)
    bio = models.TextField(max_length=500, null=True)
    born = models.DateField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    national = models.CharField(max_length=20, null=True)
    phone_verified = models.BooleanField(default=False)
    using_sites = models.ManyToManyField('ConsumerSite', related_query_name='users', related_name='users', blank=True)
    image = models.ImageField(upload_to='user_photos', blank=True)

class ConsumerSite(models.Model):
    owners = models.ManyToManyField(Profile, related_query_name='providingSites', related_name='providingSites')
    public_key = models.CharField(max_length=50)
    private_key = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)


class DynamicField(models.Model):
    field_name = models.CharField(max_length=50, primary_key=True)
    field_type = models.CharField(max_length=50, choices=get_choices(field_types))
    explanation = models.TextField(max_length=500, null=True)

    class Meta:
        unique_together = ('field_name', 'field_type')


class DesiredCharField(models.Model):
    profile = models.ForeignKey(Profile, related_query_name='DesiredCharFields', related_name='DesiredCharFields',
                                on_delete=models.CASCADE)
    field_name = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    field = models.CharField(max_length=50)

    class Meta:
        unique_together = ('profile', 'field_name')


class DesiredTextField(models.Model):
    profile = models.ForeignKey(Profile, related_query_name='DesiredTextFields', related_name='DesiredTextFields',
                                on_delete=models.CASCADE)
    field_name = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    field = models.TextField(max_length=500, null=True)

    class Meta:
        unique_together = ('profile', 'field_name')


class DesiredIntegerField(models.Model):
    profile = models.ForeignKey(Profile, related_query_name='DesiredBigIntFields', related_name='DesiredBigIntFields',
                                on_delete=models.CASCADE)
    field_name = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    field = models.BigIntegerField(default=0)

    class Meta:
        unique_together = ('profile', 'field_name')


class DesiredBooleanField(models.Model):
    profile = models.ForeignKey(Profile, related_query_name='DesiredBools', related_name='DesiredBools',
                                on_delete=models.CASCADE)
    field_name = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    field = models.BooleanField()

    class Meta:
        unique_together = ('profile', 'field_name')


class DesiredImageField(models.Model):
    profile = models.ForeignKey(Profile, related_query_name='DesiredImageFields', related_name='DesiredImageFields',
                                on_delete=models.CASCADE)
    field_name = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    field = models.ImageField(upload_to='assets/profiles', null=True)

    class Meta:
        unique_together = ('profile', 'field_name')


class DesiredEmailField(models.Model):
    profile = models.ForeignKey(Profile, related_query_name='DesiredEmailFields', related_name='DesiredEmailFields',
                                on_delete=models.CASCADE)
    field_name = models.ForeignKey(DynamicField, on_delete=models.CASCADE)
    field = models.EmailField(max_length=70)

    class Meta:
        unique_together = ('profile', 'field_name')


class PendingAccount(models.Model):
    phone = PhoneNumberField(null=False, blank=False, db_index=True)
    verification_code = models.IntegerField()
