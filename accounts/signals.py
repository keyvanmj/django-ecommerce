from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save,sender=User)
def add_default_group(sender,instance,created,**kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='customer'))