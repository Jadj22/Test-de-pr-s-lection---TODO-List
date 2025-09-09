from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Projet(models.Model):
    """
    Modèle représentant un projet dans l'application.
    Un projet appartient à un utilisateur et peut contenir plusieurs tâches.
    """
    class StatutProjet(models.TextChoices):
        A_FAIRE = 'a_faire', _('À faire')
        EN_COURS = 'en_cours', _('En cours')
        TERMINE = 'termine', _('Terminé')
    
    titre = models.CharField(_('titre'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    statut = models.CharField(
        _('statut'),
        max_length=10,
        choices=StatutProjet.choices,
        default=StatutProjet.A_FAIRE
    )
    proprietaire = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projets',
        verbose_name=_('propriétaire')
    )
    date_creation = models.DateTimeField(_('date de création'), auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(_('date de mise à jour'), auto_now=True)

    class Meta:
        verbose_name = _('projet')
        verbose_name_plural = _('projets')
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre
