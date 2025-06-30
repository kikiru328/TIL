from celery import shared_task
import logging
from search import es_client

logger = logging.getLogger(__name__)

@shared_task
def index_post_to_es(post_id):
    from posts.models import Post
    from search.documents import PostDocument

    try:
        post = Post.objects.get(id=post_id)

        doc = PostDocument(
            meta={'id': post.id},
            title=post.title,
            content=post.content,
            author=post.author.username,
            created_at=post.created_at,
        )
        doc.save()

        logger.info(f"[ElasticSearch] Post {post_id} successfully indexed.")

    except Exception as e:
        logger.error(f"[ElasticSearch] Failed to index post {post_id}: {e}")
