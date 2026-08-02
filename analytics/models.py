from django.db import models

class CAJournalier(models.Model):
    date_ca = models.DateField(unique=True)
    montant_ca = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 't_ca_journalier'
        managed = False  # Déjà géré sur PostgreSQL/Neon

    def __str__(self):
        return f"{self.date_ca} : {self.montant_ca} MGA"
