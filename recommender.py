from django.db.models import Sum
from django.contrib.auth.models import User
from .models import Product,  Customer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class Recommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.product_matrix = None
        self.products = None
        self.fit_products()

    def fit_products(self):
        """Précalcule la matrice de similarité pour les produits."""
        try:
            self.products = Product.objects.all()
            # Combiner catégorie et description pour la vectorisation
            product_features = [
                f"{p.category.name} {p.description or ''}" for p in self.products
            ]
            self.product_matrix = self.vectorizer.fit_transform(product_features)
            logger.info("Matrice de similarité des produits générée avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la matrice: {str(e)}")

    def get_content_based_recommendations(self, product_id, num_recommendations=5):
        """Recommande des produits similaires à un produit donné."""
        try:
            product_idx = list(self.products.values_list('id', flat=True)).index(product_id)
            similarity_scores = cosine_similarity(
                self.product_matrix[product_idx], self.product_matrix
            ).flatten()
            # Trier par score décroissant, exclure le produit lui-même
            similar_indices = similarity_scores.argsort()[-(num_recommendations + 1):-1][::-1]
            recommended_products = [self.products[i] for i in similar_indices]
            logger.info(f"Recommandations basées sur le contenu pour product_id={product_id}: {[p.name for p in recommended_products]}")
            return recommended_products
        except Exception as e:
            logger.error(f"Erreur dans content_based_recommendations: {str(e)}")
            return []

    def get_popularity_based_recommendations(self, num_recommendations=5):
        """Recommande les produits les plus vendus."""
        try:
            popular_products = Product.objects.annotate(
                total_sales=Sum('orderplaced__quantity')
            ).order_by('-total_sales')[:num_recommendations]
            logger.info(f"Recommandations basées sur la popularité: {[p.name for p in popular_products]}")
            return list(popular_products)
        except Exception as e:
            logger.error(f"Erreur dans popularity_based_recommendations: {str(e)}")
            return []

    def get_city_based_recommendations(self, user, num_recommendations=5):
        """Recommande les produits populaires dans la ville de l'utilisateur."""
        try:
            customer = Customer.objects.filter(user=user).first()
            if not customer or not customer.city:
                logger.warning(f"Aucune ville trouvée pour l'utilisateur {user.username}")
                return self.get_popularity_based_recommendations(num_recommendations)
            popular_in_city = Product.objects.filter(
                orderplaced__customer__city=customer.city
            ).annotate(
                total_sales=Sum('orderplaced__quantity')
            ).order_by('-total_sales')[:num_recommendations]
            logger.info(f"Recommandations basées sur la ville {customer.city} pour {user.username}: {[p.name for p in popular_in_city]}")
            return list(popular_in_city)
        except Exception as e:
            logger.error(f"Erreur dans city_based_recommendations: {str(e)}")
            return []

    def get_hybrid_recommendations(self, user, product_id=None, num_recommendations=5):
        """Combine contenu, popularité, et contexte local."""
        try:
            recommendations = []
            # 1. Si un product_id est fourni (par exemple, page produit), ajouter des recommandations basées sur le contenu
            if product_id:
                content_recs = self.get_content_based_recommendations(product_id, num_recommendations // 2)
                recommendations.extend(content_recs)
            # 2. Ajouter des recommandations basées sur la ville
            city_recs = self.get_city_based_recommendations(user, num_recommendations // 2)
            recommendations.extend(city_recs)
            # 3. Compléter avec des recommandations basées sur la popularité si nécessaire
            if len(recommendations) < num_recommendations:
                popularity_recs = self.get_popularity_based_recommendations(
                    num_recommendations - len(recommendations)
                )
                recommendations.extend(popularity_recs)
            # Supprimer les doublons et limiter au nombre demandé
            seen = set()
            unique_recommendations = []
            for rec in recommendations:
                if rec.id not in seen:
                    seen.add(rec.id)
                    unique_recommendations.append(rec)
            logger.info(f"Recommandations hybrides pour user={user.username}, product_id={product_id}: {[p.name for p in unique_recommendations[:num_recommendations]]}")
            return unique_recommendations[:num_recommendations]
        except Exception as e:
            logger.error(f"Erreur dans hybrid_recommendations: {str(e)}")
            return []
