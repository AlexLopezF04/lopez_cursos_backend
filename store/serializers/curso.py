from rest_framework import serializers
from store.models import Curso
from .usuario import UsuarioSerializer
from .categoria import CategoriaSerializer

class CursoListSerializer(serializers.ModelSerializer):
    """Versión liviana para listados."""
    instructor   = serializers.SerializerMethodField()
    categoria    = serializers.SerializerMethodField()
    categoria_id = serializers.PrimaryKeyRelatedField(
        source='categoria', read_only=True,
    )

    class Meta:
        model  = Curso
        fields = [
            'id', 'titulo', 'descripcion', 'nivel', 'precio',
            'publicado', 'instructor', 'categoria', 'categoria_id',
            'created_at', 'updated_at',
        ]

    def get_instructor(self, obj):
        return {'id': obj.instructor_id, 'username': obj.instructor.username}

    def get_categoria(self, obj):
        if obj.categoria is None:
            return None
        return {'id': obj.categoria.id, 'nombre': obj.categoria.nombre}

class CursoSerializer(serializers.ModelSerializer):
    """Versión completa para detalle / creación."""
    instructor = UsuarioSerializer(read_only=True)
    categoria  = CategoriaSerializer(read_only=True)

    categoria_id  = serializers.PrimaryKeyRelatedField(
        source='categoria', queryset=__import__('store.models', fromlist=['Categoria']).Categoria.objects.all(),
        write_only=True, allow_null=True, required=False,
    )

    class Meta:
        model  = Curso
        fields = [
            'id', 'titulo', 'descripcion', 'precio', 'nivel',
            'publicado', 'instructor', 'categoria', 'categoria_id', 'created_at', 'updated_at',
        ]
        read_only_fields = ['instructor', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['instructor'] = self.context['request'].user
        return super().create(validated_data)