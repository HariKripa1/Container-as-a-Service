from rest_framework import permissions



class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #if request.method in permissions.SAFE_METHODS:
         #   return True

        # Write permissions are only allowed to the owner of the snippet.
        #print 'hoho'
        #print request.user.username
        #print obj.user_id.username
        return obj.user_id == request.user