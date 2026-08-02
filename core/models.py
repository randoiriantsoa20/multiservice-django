from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password as django_check_password

# --- GESTIONNAIRE & MODÈLE UTILISATEUR ---

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

    @password.setter
    def password(self, raw_password):
        if raw_password:
            self.mot_de_passe = make_password(raw_password)

    def set_password(self, raw_password):
        if raw_password:
            self.mot_de_passe = make_password(raw_password)

    def check_password(self, raw_password):
        if not self.mot_de_passe:
            return False
        return django_check_password(raw_password, self.mot_de_passe)

    def has_usable_password(self):
        return bool(self.mot_de_passe)

    @property
    def is_staff(self):
        return True

    @property
    def is_superuser(self):
        return self.role_privilege in ['admin', 'superuser']

    @property
    def is_active(self):
        return True

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.identifiant or f"Utilisateur #{self.id_utilisateur}"


# --- MODÈLES MÉTIERS NEON POSTGRESQL ---

class Operateur(models.Model):
    id_operateur = models.AutoField(primary_key=True)
    nom_operateur = models.CharField(max_length=50, unique=True, verbose_name="Nom de l'opérateur")
    role_operateur = models.CharField(max_length=50, blank=True, null=True, verbose_name="Rôle")
    utilisateur = models.OneToOneField(
        Utilisateur, 
        on_delete=models.DO_NOTHING, 
        db_column='id_utilisateur', 
        unique=True, 
        blank=True, 
        null=True,
        verbose_name="Compte Utilisateur"
    )

    class Meta:
        db_table = 't_operateur'
        managed = False
        verbose_name = "Opérateur"
        verbose_name_plural = "Opérateurs"

    def __str__(self):
        return self.nom_operateur


class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    libelle_service = models.CharField(max_length=50, unique=True, verbose_name="Libellé du service")
    tarif = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tarif")
    temps_estime_mn = models.IntegerField(blank=True, null=True, verbose_name="Temps estimé (min)")

    class Meta:
        db_table = 't_service'
        managed = False
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.libelle_service


class CaJournalier(models.Model):
    date_ca = models.DateField(primary_key=True, verbose_name="Date")
    montant_ca = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Chiffre d'Affaires")

    class Meta:
        db_table = 't_ca_journalier'
        managed = False
        verbose_name = "CA Journalier"
        verbose_name_plural = "Chiffres d'Affaires Journaliers"

    def __str__(self):
        return f"{self.date_ca} - {self.montant_ca} Ar"


class Depense(models.Model):
    id = models.AutoField(primary_key=True)
    source_depense = models.CharField(max_length=100, blank=True, null=True, verbose_name="Source / Catégorie")
    libelle = models.CharField(max_length=255, verbose_name="Description / Libellé")
    date_depense = models.DateField(verbose_name="Date de dépense")
    montant_virement = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant")

    class Meta:
        db_table = 't_depenses'
        managed = False
        verbose_name = "Dépense"
        verbose_name_plural = "Dépenses"

    def __str__(self):
        return f"{self.libelle} ({self.montant_virement})"


class Production(models.Model):
    id_production = models.AutoField(primary_key=True)
    date_production = models.DateTimeField(verbose_name="Date & Heure")
    quantite = models.IntegerField(default=1, verbose_name="Quantité")
    montant_encaisse = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant encaissé")
    operateur = models.ForeignKey(
        Operateur, 
        on_delete=models.DO_NOTHING, 
        db_column='id_operateur', 
        blank=True, 
        null=True,
        verbose_name="Opérateur"
    )
    service = models.ForeignKey(
        Service, 
        on_delete=models.DO_NOTHING, 
        db_column='id_service', 
        blank=True, 
        null=True,
        verbose_name="Service"
    )
    remarques = models.TextField(blank=True, null=True, verbose_name="Remarques")

    class Meta:
        db_table = 't_production'
        managed = False
        verbose_name = "Production / Transaction"
        verbose_name_plural = "Productions / Transactions"

    def __str__(self):
        return f"Prod #{self.id_production} - {self.montant_encaisse}"
