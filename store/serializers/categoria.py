from django.utils.text import slugify
from rest_framework import serializers
from store.models import Categoria

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Categoria
        fields = ['id', 'nombre', 'slug']
        extra_kwargs = {'slug': {'required': False}}

    def create(self, validated_data):
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data['nombre'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'slug' not in validated_data or not validated_data['slug']:
            validated_data['slug'] = slugify(validated_data.get('nombre', instance.nombre))
        return super().update(instance, validated_data)