from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.hashers import make_password, check_password as django_check_password

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

    # 1. Alias obligatoire pour que Django voie le champ physique `mot_de_passe` comme `password`
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

    # 2. Forcer Django à valider que le mot de passe est exploitable
    def has_usable_password(self):
        return bool(self.mot_de_passe)

    # 3. Méthodes de permissions indispensables pour l'interface Admin
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
        return self.identifiant
        
        

# --- Nouveaux modèles métiers pour le Multiservice ---

class Service(models.Model):
    id_service = models.AutoField(primary_key=True)
    nom_service = models.CharField(max_length=150, verbose_name="Nom du service")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    tarif_base = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Tarif de base")
    est_actif = models.BooleanField(default=True, verbose_name="Actif")

    class Meta:
        db_table = 't_service'
        managed = False
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.nom_service


class Transaction(models.Model):
    id_transaction = models.AutoField(primary_key=True)
    date_heure = models.DateTimeField(auto_now_add=True, verbose_name="Date & Heure")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, db_column='id_service', verbose_name="Service")
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.DO_NOTHING, db_column='id_utilisateur', verbose_name="Opérateur")
    montant = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Montant (Ar/FCFA/$)")
    mode_paiement = models.CharField(max_length=50, default='Espece', verbose_name="Mode de paiement")
    remarques = models.CharField(max_length=255, blank=True, null=True, verbose_name="Notes / Détails")

    class Meta:
        db_table = 't_transaction'
        managed = False
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"

    def __str__(self):
        return f"Transaction #{self.id_transaction} - {self.montant}"


class CaisseJournaliere(models.Model):
    id_caisse = models.AutoField(primary_key=True)
    date_jour = models.DateField(unique=True, verbose_name="Date du jour")
    fond_de_caisse = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Fond de caisse initial")
    total_entrees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Encaissements")
    total_sorties = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Total Dépenses")
    solde_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Solde de clôture")
    est_cloturee = models.BooleanField(default=False, verbose_name="Caisse Clôturée")

    class Meta:
        db_table = 't_caisse_journaliere'
        managed = False
        verbose_name = "Caisse Journalière"
        verbose_name_plural = "Caisses Journalières"

    def __str__(self):
        return f"Caisse du {self.date_jour}"