from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Avatar"
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Biographie"
    )
    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['username']

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nom de la catégorie")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

class Activity(models.Model):
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(verbose_name="Description")
    location_city = models.CharField(max_length=100, verbose_name="Ville")
    start_time = models.DateTimeField(verbose_name="Date et heure de début")
    end_time = models.DateTimeField(verbose_name="Date et heure de fin")
    proposer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposed_activities', verbose_name="Organisateur")
    attendees = models.ManyToManyField(User, blank=True, related_name='attended_activities', verbose_name="Participants")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='activities', verbose_name="Catégorie")

    def clean(self):
        super().clean()

        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError({
                    'end_time': 'La date de fin doit être postérieure à la date de début.'
                })

        if self.start_time and not self.pk:
            if self.start_time <= timezone.now():
                raise ValidationError({
                    'start_time': 'La date de début doit être dans le futur.'
                })

        if self.description and len(self.description.strip()) < 10:
            raise ValidationError({
                'description': 'La description doit contenir au minimum 10 caractères.'
            })

        if self.title and (len(self.title.strip()) < 5 or len(self.title.strip()) > 200):
            raise ValidationError({
                'title': 'Le titre doit contenir entre 5 et 200 caractères.'
            })

        if self.location_city and (len(self.location_city.strip()) < 2 or len(self.location_city.strip()) > 100):
            raise ValidationError({
                'location_city': 'La ville doit contenir entre 2 et 100 caractères.'
            })

    def save(self, *args, **kwargs):
        """Override save pour appeler clean() automatiquement."""
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Activité"
        verbose_name_plural = "Activités"
        ordering = ['start_time']
