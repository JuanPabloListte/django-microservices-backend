from apps.category.serializers import CategorySerializer
from rest_framework.views import APIView
from rest_framework_api.views import StandardAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Category, ViewCount
from rest_framework.pagination import PageNumberPagination
from slugify import slugify
from django.core.cache import cache


class PrimaryCategoriesView(StandardAPIView):
    def get(self, request, format=None):
        primary_categories = Category.objects.filter(parent=None)
        category_names = [category.name for category in primary_categories]
        return self.send_response(category_names, status=status.HTTP_200_OK)
    

class SubCategoriesView(StandardAPIView):
    def get(self, request, slug):
        try:
            parent_category = Category.objects.get(slug=slug)
            sub_categories = parent_category.children.all()
            sub_category_names = [category.name for category in sub_categories]
            return self.send_response(sub_category_names, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return self.send_error("Parent category does not exist.", status=status.HTTP_404_NOT_FOUND)
        
class TertiaryCategoriesView(StandardAPIView):
    def get(self, request, slug):
        try:
            parent_category = Category.objects.get(slug=slug)
            print(parent_category)
            tertiary_categories = parent_category.children.all()
            tertiary_category_names = [category.name for category in tertiary_categories]
            return self.send_response(tertiary_category_names, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return self.send_error("Parent category does not exist.", status=status.HTTP_404_NOT_FOUND)
        
class ListCategoriesView(StandardAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, format=None):
        if Category.objects.all().exists():
            categories = Category.objects.all()

            result = []

            for category in categories:
                if not category.parent:
                    item = {}
                    item['id']=category.id
                    item['name']=category.name
                    item['title']=category.title
                    item['description']=category.description
                    item['slug']=category.slug
                    item['views']=category.views
                
                    item['sub_categories'] = []
                    for sub_category in categories:
                        sub_item = {}
                        if sub_category.parent and sub_category.parent.id == category.id:
                            sub_item['id']=sub_category.id
                            sub_item['name']=sub_category.name
                            sub_item['title']=sub_category.title
                            sub_item['description']=sub_category.description
                            sub_item['slug']=sub_category.slug
                            sub_item['views']=sub_category.views

                            item['sub_categories'].append(sub_item)

                            sub_item['sub_categories'] = []
                            for sub_sub_category in categories.filter(parent=sub_category):
                                sub_sub_item = {}
                                if sub_sub_category.parent and sub_sub_category.parent.id == sub_category.id:
                                    sub_sub_item['id'] = sub_sub_category.id
                                    sub_sub_item['name'] = sub_sub_category.name
                                    sub_sub_item['title'] = sub_sub_category.title
                                    sub_sub_item['description'] = sub_sub_category.description
                                    sub_sub_item['slug'] = sub_sub_category.slug
                                    sub_sub_item['views']= sub_sub_category.views
                                    
                                    sub_item['sub_categories'].append(sub_sub_item)
                    
                    result.append(item)

            return self.send_response(result, status=status.HTTP_200_OK)
        else:
            return self.send_error('No categories found', status=status.HTTP_404_NOT_FOUND)
