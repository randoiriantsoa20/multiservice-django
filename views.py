from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear, ExtractDay
from .models import CAJournalier  # Adaptez selon le nom exact de votre modèle Django

def dashboard_ca(request):
    # 1. Sélection des années disponibles pour les filtres
    years_available = (
        CAJournalier.objects.annotate(year=ExtractYear('date_ca'))
        .values_list('year', flat=True)
        .distinct()
        .order_by('-year')
    )
    
    selected_year = int(request.GET.get('year', years_available[0] if years_available else 2026))

    # 2. CA Total par Année
    ca_yearly = (
        CAJournalier.objects.annotate(year=ExtractYear('date_ca'))
        .values('year')
        .annotate(total_ca=Sum('montant_ca'))
        .order_by('year')
    )

    # 3. CA Mensuel pour l'année sélectionnée
    ca_monthly = (
        CAJournalier.objects.filter(date_ca__year=selected_year)
        .annotate(month=ExtractMonth('date_ca'))
        .values('month')
        .annotate(total_ca=Sum('montant_ca'))
        .order_by('month')
    )

    # 4. Comparatif Interannuel même jour (ex: 15 Juillet 2025 vs 15 Juillet 2026)
    day_cmp = int(request.GET.get('day', 15))
    month_cmp = int(request.GET.get('month', 7))
    year1_cmp = int(request.GET.get('year1', 2025))
    year2_cmp = int(request.GET.get('year2', 2026))

    obj_y1 = CAJournalier.objects.filter(
        date_ca__year=year1_cmp, date_ca__month=month_cmp, date_ca__day=day_cmp
    ).first()
    obj_y2 = CAJournalier.objects.filter(
        date_ca__year=year2_cmp, date_ca__month=month_cmp, date_ca__day=day_cmp
    ).first()

    ca_y1 = float(obj_y1.montant_ca) if obj_y1 else 0.0
    ca_y2 = float(obj_y2.montant_ca) if obj_y2 else 0.0
    diff = ca_y2 - ca_y1
    growth = round(((diff / ca_y1) * 100), 2) if ca_y1 > 0 else 0.0

    context = {
        'years_available': years_available,
        'selected_year': selected_year,
        'ca_yearly_labels': [item['year'] for item in ca_yearly],
        'ca_yearly_data': [float(item['total_ca']) for item in ca_yearly],
        'ca_monthly_labels': [f"Mois {item['month']}" for item in ca_monthly],
        'ca_monthly_data': [float(item['total_ca']) for item in ca_monthly],
        'comparison': {
            'day': day_cmp,
            'month': month_cmp,
            'year1': year1_cmp,
            'year2': year2_cmp,
            'ca_y1': ca_y1,
            'ca_y2': ca_y2,
            'diff': diff,
            'growth': growth,
        }
    }
    return render(request, 'dashboard.html', context)
