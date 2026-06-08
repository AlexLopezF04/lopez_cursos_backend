from django.db.models.signals import post_save
from django.dispatch import receiver
from store.models import Matricula, Progreso, Leccion

@receiver(post_save, sender=Matricula)
def crear_progresos_al_matricular(sender, instance, created, **kwargs):
    if not created:
        return
    lecciones = Leccion.objects.filter(curso=instance.curso)
    progresos = [
        Progreso(matricula=instance, leccion=lec, completada=False)
        for lec in lecciones
    ]
    Progreso.objects.bulk_create(progresos, ignore_conflicts=True)
