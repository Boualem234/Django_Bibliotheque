from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver

from .models import Product


@receiver(post_delete, sender=Product)
def product_post_delete(sender, instance, **kwargs):
  # Permet de supprimer l'image du produit sur le disque.
  instance.image.delete(False) # Passez False pour ne pas enregistrer le modèle.

@receiver(pre_save, sender=Product)
def product_pre_save(sender, instance, **kwargs):
  if instance.pk:
    try:
      old_image = sender.objects.get(pk=instance.pk).image
      if old_image != instance.image:
        # Permet de supprimer l'ancienne image du produit sur le disque si modifiée.
        old_image.delete(False) # Passez False pour ne pas enregistrer le modèle.
    except Product.DoesNotExist:
      pass
