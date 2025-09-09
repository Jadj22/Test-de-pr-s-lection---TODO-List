from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from projects.models import Projet

class Tache(models.Model):
    """
    Modèle représentant une tâche dans l'application.
    Une tâche appartient à un projet et peut avoir différents statuts.
    """
    class StatutTache(models.TextChoices):
        A_FAIRE = 'a_faire', _('À faire')
        EN_COURS = 'en_cours', _('En cours')
        TERMINEE = 'terminee', _('Terminée')
    
    class PrioriteTache(models.TextChoices):
        BASSE = 'basse', _('Basse')
        NORMALE = 'normale', _('Normale')
        HAUTE = 'haute', _('Haute')
    
    titre = models.CharField(_('titre'), max_length=200)
    description = models.TextField(_('description'), blank=True)
    statut = models.CharField(
        _('statut'),
        max_length=10,
        choices=StatutTache.choices,
        default=StatutTache.A_FAIRE
    )
    projet = models.ForeignKey(
        Projet,
        on_delete=models.CASCADE,
        related_name='taches',
        verbose_name=_('projet')
    )
    date_echeance = models.DateTimeField(_('date d\'échéance'), null=True, blank=True)
    priorite = models.CharField(
        _('priorité'),
        max_length=10,
        choices=PrioriteTache.choices,
        default=PrioriteTache.NORMALE
    )
    date_accomplissement = models.DateTimeField(_('date d\'accomplissement'), null=True, blank=True)
    date_creation = models.DateTimeField(_('date de création'), auto_now_add=True)
    date_mise_a_jour = models.DateTimeField(_('date de mise à jour'), auto_now=True)
    cree_par = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='taches_crees',
        verbose_name=_('créé par')
    )
    assigne_a = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='taches_assignees',
        verbose_name=_('assigné à')
    )

    class Meta:
        verbose_name = _('tâche')
        verbose_name_plural = _('tâches')
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre
