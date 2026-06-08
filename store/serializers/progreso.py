from rest_framework import serializers
from store.models import Progreso
from django.utils import timezone

class ProgresoSerializer(serializers.ModelSerializer):
    leccion_titulo  = serializers.CharField(source='leccion.titulo',  read_only=True)
    curso_titulo    = serializers.CharField(source='leccion.curso.titulo', read_only=True)
    curso_id        = serializers.IntegerField(source='leccion.curso.id',   read_only=True)

    class Meta:
        model  = Progreso
        fields = [
            'id', 'matricula', 'leccion', 'leccion_titulo',
            'curso_id', 'curso_titulo', 'completada', 'fecha_completado',
        ]
        read_only_fields = ['fecha_completado']

    def update(self, instance, validated_data):
        if validated_data.get('completada') and not instance.completada:
            validated_data['fecha_completado'] = timezone.now()
        return super().update(instance, validated_data)