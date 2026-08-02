from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from django.contrib.auth.backends import BaseBackend

class UtilisateurManager(BaseUserManager):
    def create_user(self, identifiant, password=None, **extra_fields):
        if not identifiant:
            raise ValueError("L'identifiant est obligatoire")
        user = self.model(identifiant=identifiant, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifiant, password=None, **extra_fields):
        extra_fields.setdefault('role_privilege', 'admin')
        return self.create_user(identifiant, password, **extra_fields)

class Utilisateur(AbstractBaseUser, PermissionsMixin):
    id_utilisateur = models.AutoField(primary_key=True)
    identifiant = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=255, db_column='mot_de_passe')
    nom_complet = models.CharField(max_length=100, blank=True, null=True)
    role_privilege = models.CharField(max_length=30, default='user')
    date_creation = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'identifiant'
    REQUIRED_FIELDS = []

    objects = UtilisateurManager()

    class Meta:
        db_table = 't_utilisateur'
        managed = False

    @property
    def password(self):
        return self.mot_de_passe

    def set_password(self, raw_password):
        if raw_password:
            self.mot_de_passe = make_password(raw_password)

    def check_password(self, raw_password):
        if not self.mot_de_passe:
            return False
        return django_check_password(raw_password, self.mot_de_passe)

    @property
    def is_staff(self):
        return True

    @property
    def is_superuser(self):
        return self.role_privilege in ['admin', 'superuser']

    @property
    def is_active(self):
        return True

    def __str__(self):
        return self.identifiant

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get('identifiant')
        try:
            user = Utilisateur.objects.get(identifiant=username)
            if user.check_password(password):
                return user
        except Utilisateur.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Utilisateur.objects.get(pk=user_id)
        except Utilisateur.DoesNotExist:
            return None
