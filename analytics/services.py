from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
from .models import CAJournalier

class CAService:
    @staticmethod
    def get_available_years():
        return list(
            CAJournalier.objects.annotate(year=ExtractYear('date_ca'))
            .values_list('year', flat=True)
            .distinct()
            .order_by('-year')
        )

    @staticmethod
    def get_yearly_aggregates():
        results = (
            CAJournalier.objects.annotate(year=ExtractYear('date_ca'))
            .values('year')
            .annotate(total_ca=Sum('montant_ca'))
            .order_by('year')
        )
        return {
            'labels': [item['year'] for item in results],
            'data': [float(item['total_ca']) for item in results]
        }

    @staticmethod
    def get_monthly_aggregates(year):
        results = (
            CAJournalier.objects.filter(date_ca__year=year)
            .annotate(month=ExtractMonth('date_ca'))
            .values('month')
            .annotate(total_ca=Sum('montant_ca'))
            .order_by('month')
        )
        return {
            'labels': [f"Mois {item['month']}" for item in results],
            'data': [float(item['total_ca']) for item in results]
        }

    @staticmethod
    def compare_daily_stats(day, month, year1, year2):
        obj_y1 = CAJournalier.objects.filter(
            date_ca__year=year1, date_ca__month=month, date_ca__day=day
        ).first()
        obj_y2 = CAJournalier.objects.filter(
            date_ca__year=year2, date_ca__month=month, date_ca__day=day
        ).first()

        ca_y1 = float(obj_y1.montant_ca) if obj_y1 else 0.0
        ca_y2 = float(obj_y2.montant_ca) if obj_y2 else 0.0
        diff = ca_y2 - ca_y1
        growth = round(((diff / ca_y1) * 100), 2) if ca_y1 > 0 else 0.0

        return {
            'day': day, 'month': month, 'year1': year1, 'year2': year2,
            'ca_y1': ca_y1, 'ca_y2': ca_y2, 'diff': diff, 'growth': growth
        }
