from collections import defaultdict
from dolphin_v3.cache.redis_cache import get_redis_client
from django.contrib.auth.models import  Group, Permission
from django.contrib.auth.models import AnonymousUser

from django.urls import resolve
from rest_framework.permissions import BasePermission
from django.core.exceptions import ImproperlyConfigured
from rest_framework.exceptions import PermissionDenied

class PermissionUtils:
    '''
    Utility class for handling user permissions based on groups and caching.
    Models used: User, Group, Permission (django default models)
    :param
    :user : User instance
    :model : Django Model class()
    :view : View instance
    :request : Request instance

    Usage:
        permission_utils = PermissionUtils(user=request.user, model=SomeModel)
        has_perm = permission_utils.has_permission('view')

        django saves the permissions in the format by default: 'action_modelname'
        where action can be: 'view', 'add', 'change', 'delete'
    '''
    def __init__(self, user = None, model=None, view=None, request=None):
        self.user = user
        self.model = model
        self.view = view
        self.request = request
        self.actions = {
            'view': 'list',
            'add': 'create',
            'change': 'update',
            'delete': 'delete'
        }
    
    def has_permission(self, action):
        '''
        Check if the user has the required permission for the given action on the model.
        Uses cache to reduce DB queries.

        :param action: 'view', 'add', 'change', 'delete'
        :return: Boolean
        '''
        if action not in self.actions.keys():
            raise ValueError(f"Invalid action: {action}. Valid actions are: {list(self.actions.keys())}")

        # Superuser always has permission
        if self.user.is_superuser:
            return True

        # Create a cache key based on user id, model name, and action
        cache_key = f"user_perm:{self.user.id}:{self.model._meta.model_name.lower()}:{action}"

        try:
        # Try to get cached result
            cached_result = get_redis_client("default").get(cache_key)
        except Exception as e:
            cached_result = None
            
        # cached_result = cache.get(cache_key)
        if cached_result is not None:
            return cached_result

        # Check group permissions
        user_groups = self.user.groups.all()
        required_permission = f'{action}_{self.model._meta.model_name}'
        has_perm = False
        for group in user_groups:
            if group.permissions.filter(codename=required_permission).exists():
                has_perm = True
                break
        try:
            # Cache the result for future use
            get_redis_client("default").set(cache_key, has_perm, ttl=300)  # 300 seconds = 5 minutes
        except Exception as e:
            pass
        
        return has_perm
    
    def get_user_all_permissions(self):
        '''
        Get all permissions for the given user.
        :param user: User instance
        :return: Set of permission codenames
        '''
        if self.user.is_superuser:
            return set(Permission.objects.values_list('codename', flat=True))
        
        user_groups = self.user.groups.all()
        permissions = set()
        for group in user_groups:
            group_permissions = group.permissions.values_list('codename', flat=True)
            permissions.update(group_permissions)
        return permissions
    
    def user_available_actions(self):
        '''
        Get all available actions for the user on the model.
        :return: List of actions
        '''
        available_actions = []
        for action in self.actions.keys():
            if self.has_permission(action):
                available_actions.append(action)
        return available_actions

    def get_user_model_permissions(self):
        '''
        Get all permissions for the user related to the model.
        :return: Set of permission codenames
        '''
        if self.user.is_superuser:
            return set(Permission.objects.filter(content_type__model=self.model._meta.model_name).values_list('codename', flat=True))
        
        user_groups = self.user.groups.all()
        permissions = set()
        for group in user_groups:
            group_permissions = group.permissions.filter(content_type__model=self.model._meta.model_name).values_list('codename', flat=True)
            permissions.update(group_permissions)
        return permissions
    
    @staticmethod
    def get_all_permissions():
        '''
        Get all permissions grouped by model name.
        :return: dict
        '''
        if get_redis_client("default") is not None:
            cache_key = "all_permissions_dict"
            try:
                cached_permissions = get_redis_client("default").get(cache_key)
                if cached_permissions is not None:
                    return cached_permissions
            except Exception as e:
                pass
            
        permissions = Permission.objects.select_related(
            "content_type"
        ).values(
            "id",
            "name",
            "codename",
            "content_type__model",
        )

        result = defaultdict(list)

        for perm in permissions:
            model_name = perm["content_type__model"]

            result[model_name].append({
                "id": perm["id"],
                "name": perm["name"],
                "code": perm["codename"],
            })
        cache_key = "all_permissions_dict"
        try:
            get_redis_client("default").set(cache_key, dict(result), ttl=3600)  # Cache for 1 hour
        except Exception as e:
            pass


        return dict(result)
    
    
class CustomPermissionClass(BasePermission):
    '''
    Custom permission class to check user permissions based on action and model.
    Usage:
        - permission_classes = [CustomPermissionClass]
        - permissions = {
            'all': 'user-module',
            'list': 'can_view_user-module',
            'create': 'can_add_user-module',
            'update': 'can_update_user-module',
            'delete': 'can_delete_user-module',
          }
    '''
    def has_permission(self, request, view):
        try:
            method_action = {
                "GET": "view",
                "POST": "add",
                "PUT": "change",
                "PATCH": "change",
                "DELETE": "delete",
            }
            if not request.user or isinstance(request.user, AnonymousUser):
                return False
            if request.method in ["OPTIONS", "HEAD"]:
                return True
            user = request.user
            if user.is_superuser:
                return True
            if hasattr(view, "get_queryset"):
                model = view.get_queryset().model
            elif hasattr(view, "queryset") and view.queryset is not None:
                model = view.queryset.model
            else:
                raise ImproperlyConfigured("CustomPermissionClass requires a queryset on the view.")
            
            permission_utils = PermissionUtils(user=user, model=model, view=view, request=request)

            # Map HTTP methods to action keys
            action_key = method_action.get(request.method.upper())

            if not action_key:
                return False
            
            has_module_permission = permission_utils.has_permission(action_key)

            return bool(has_module_permission)
        
        except ImproperlyConfigured as e:
            raise e
        except Exception as e:
            raise e
            # return False

class IsSuperUser(BasePermission):
    '''
    Custom permission class to allow only superusers.
    Usage:
        - permission_classes = [IsSuperUser]
    '''
    def has_permission(self, request, view):
        if not request.user or isinstance(request.user, AnonymousUser):
            return False
        return request.user.is_superuser