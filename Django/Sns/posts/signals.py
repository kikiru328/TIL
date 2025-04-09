from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Post
from search.tasks import index_post_to_es

@receiver(post_save, sender=Post)
def trigger_index_post(sender, instance, **kwargs):
    index_post_to_es.delay(instance.id)
