from ecommerce.utils import random_string_generator
from django.utils.text import slugify
import datetime
import uuid


def unique_slug_generator(instance, new_transaction_id=None):
    if new_transaction_id is not None:
        t_id = new_transaction_id
    else:
        t_id = slugify(f'{instance.full_name}-{uuid.uuid4().hex[:4]}-{datetime.datetime.now().strftime("%H:%M:%S")}',instance)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(transaction_id=t_id).exists()
    if qs_exists:
        new_transaction_id = "{slug}-{randstr}".format(
            slug=t_id,
            randstr=random_string_generator(size=12)
        )
        return unique_slug_generator(instance, new_transaction_id=new_transaction_id)
    return t_id