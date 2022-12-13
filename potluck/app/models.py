from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Friend(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    current_user = models.ForeignKey(
        Profile,
        related_name="owner",
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.current_user)


class Event(models.Model):
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    start = models.DateTimeField()
    time = models.TimeField(default=now)
    description = models.TextField(max_length=2000, default='')
    attendees = models.IntegerField(default=0)
    apt = models.CharField(max_length=140, default='')
    address = models.CharField(max_length=140)
    city = models.CharField(max_length=140)
    state = models.CharField(max_length=140)
    zip_code = models.CharField(max_length=140)

    def upcoming(self):
        return now().date() < self.start.date()

    def __str__(self):
        return str(self.name)

class Guest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.profile.user.username)


class Item(models.Model):
    name = models.CharField(max_length=140)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    fulfilled = models.BooleanField(default=False),
    status = models.CharField(max_length=140, default='')
    description = models.TextField(max_length=2000, default='')
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    def get_status_display(self):
        return self.status, self.fulfilled



class Request(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    item = models.ForeignKey(
        Item, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)


class Entertainment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.CharField(max_length=140, default='')
    description = models.TextField(max_length=2000, default='')

    def __str__(self):
        return str(self.description)
