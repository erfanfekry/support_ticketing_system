from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.orders.models import Order
from apps.users.models import Driver


# @receiver(signal=m2m_changed, sender=Post.likes.through)
# def total_likes_changed(sender, instance, **kwargs):
#     instance.total_likes = instance.likes.count()
#     instance.save()

# @receiver(signal=post_delete, sender=Post)
# def post_delete_changed(signal, instance, **kwargs):
#     author = instance.author
#     subject = 'Your post was deleted'
#     message = f'Your post with title "{instance.description[:20] + "..."}" was deleted due the violation our policies.'
#     send_mail(subject, message, 'erfanfekry@gmail.com', [author.email],
#               fail_silently=False )
@receiver(signal=post_save, sender=Order)
def profile_autofill(sender, instance, **kwargs):
    if Driver.objects.count() > 0:
        random_driver = Driver.objects.first()
    else:
        random_driver = None

    if instance.status == 'SHPD' and instance.driver is None:
        instance.driver = random_driver
        instance.save()

    elif instance.status not in ['SHPD', 'DLVD'] and instance.driver:
        instance.driver = None
        instance.save()

