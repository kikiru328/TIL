from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, post):
        if request.method in SAFE_METHODS: #Get, Head, Options
            return True
        return post.author == request.user

