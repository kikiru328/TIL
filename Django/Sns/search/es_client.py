from elasticsearch_dsl import connections

from django.conf import settings

connections.create_connection(hosts=[settings.ELASTIC_SEARCH_HOST])
