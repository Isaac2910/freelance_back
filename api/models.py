from django.db import models
from django.contrib.auth.models import AbstractUser

# Enum pour les rôles
class Role(models.TextChoices):
    PROJECT_OWNER = "PROJECT_OWNER", "Project Owner"
    FREELANCER = "FREELANCER", "Freelancer"
    INTERMEDIARY = "INTERMEDIARY", "Intermediary"

# Enum pour les statuts des offres
class OfferStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    ASSIGNED = "ASSIGNED", "Assigned"
    COMPLETED = "COMPLETED", "Completed"
    CANCELLED = "CANCELLED", "Cancelled"

# Modèle utilisateur personnalisé
class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.FREELANCER
    )

    def _str_(self):
        return self.username

# Modèle pour les offres
class Offer(models.Model):
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_offers"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=OfferStatus.choices,
        default=OfferStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_offers"
    )

    def _str_(self):
        return self.title

# Modèle pour les messages
class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )
    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="received_messages"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def _str_(self):
        return f"Message from {self.sender} to {self.receiver}"