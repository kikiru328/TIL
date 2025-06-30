from elasticsearch_dsl import Document, Text, Date
from posts.models import Post

class PostDocument(Document):
    content = Text()
    author = Text()
    created_at = Date()

    class Index:
        name = "posts"