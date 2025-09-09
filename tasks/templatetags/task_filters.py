from django import template
from django.db.models import QuerySet
import logging

logger = logging.getLogger(__name__)
register = template.Library()

def debug_queryset(queryset, name="Queryset"):
    """Affiche des informations de débogage sur un QuerySet"""
    logger.info(f"=== DÉBOGAGE {name.upper()} ===")
    logger.info(f"Type: {type(queryset)}")
    logger.info(f"Taille: {len(queryset) if hasattr(queryset, '__len__') else 'N/A'}")
    
    if hasattr(queryset, 'model'):
        logger.info(f"Modèle: {queryset.model.__name__}")
    
    if hasattr(queryset, 'query'):
        logger.info(f"Requête SQL: {str(queryset.query)}")
    
    try:
        if hasattr(queryset, 'values_list'):
            stats = queryset.values_list('statut', flat=True)
            logger.info(f"Statuts uniques: {set(stats) if stats else 'Aucun'}")
    except Exception as e:
        logger.error(f"Erreur lors de l'analyse du queryset: {e}")
    
    logger.info("=== FIN DÉBOGAGE ===")

@register.filter(name='filter_statut')
def filter_statut(value, statut):
    """
    Filtre un itérable de tâches par statut.
    
    Args:
        value: Peut être un QuerySet, une liste ou un autre itérable de tâches
        statut: Le statut à filtrer (ex: 'terminee', 'en_cours', 'a_faire')
    
    Returns:
        Un itérable filtré ou une liste vide si le filtrage n'est pas possible
    """
    logger.info(f"\n=== FILTRAGE PAR STATUT: {statut} ===")
    
    # Si la valeur est None ou vide, retourner une liste vide
    if not value:
        logger.warning("Aucune donnée à filtrer (valeur None ou vide)")
        return []
    
    # Afficher des informations de débogage sur l'entrée
    debug_queryset(value, "Entrée du filtre")
    
    # Si c'est un QuerySet
    if isinstance(value, QuerySet):
        try:
            # Créer une copie du queryset pour éviter les effets de bord
            queryset = value.all()
            result = queryset.filter(statut=statut)
            logger.info(f"{result.count()} éléments correspondent au statut '{statut}' (sur {queryset.count()} au total)")
            return result
        except Exception as e:
            logger.error(f"Erreur lors du filtrage du QuerySet: {e}")
            return value.none()
    
    # Si c'est une liste ou un autre itérable
    elif hasattr(value, '__iter__'):
        try:
            # Convertir en liste si ce n'est pas déjà le cas
            items = list(value)
            
            # Filtrer les éléments qui ont un attribut 'statut' correspondant
            result = [
                item for item in items 
                if hasattr(item, 'statut') and str(getattr(item, 'statut', '')) == str(statut)
            ]
            
            logger.info(f"Filtrage de {len(items)} éléments, {len(result)} correspondent au statut '{statut}'")
            
            # Afficher un échantillon des résultats pour le débogage
            if result:
                sample = min(3, len(result))
                sample_items = [f"{item.id}: {item.statut}" for item in result[:sample]]
                logger.info(f"Exemple des {sample} premiers résultats: {', '.join(sample_items)}" + 
                          ("..." if len(result) > sample else ""))
            
            return result
            
        except Exception as e:
            logger.error(f"Erreur lors du filtrage de l'itérable: {e}")
            return []
    
    # Si le type n'est pas pris en charge
    error_msg = f"Type non pris en charge pour le filtrage: {type(value)}. Attendu: QuerySet ou itérable."
    logger.error(error_msg)
    return []
