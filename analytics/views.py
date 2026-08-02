from django.shortcuts import render
from django.views import View
from .services import CAService

class CADashboardView(View):
    template_name = 'analytics/dashboard.html'

    def get(self, request, *args, **kwargs):
        years_available = CAService.get_available_years()
        default_year = years_available[0] if years_available else 2026

        selected_year = int(request.GET.get('year', default_year))
        day_cmp = int(request.GET.get('day', 15))
        month_cmp = int(request.GET.get('month', 7))
        year1_cmp = int(request.GET.get('year1', 2025))
        year2_cmp = int(request.GET.get('year2', 2026))

        context = {
            'years_available': years_available,
            'selected_year': selected_year,
            'yearly': CAService.get_yearly_aggregates(),
            'monthly': CAService.get_monthly_aggregates(selected_year),
            'comparison': CAService.compare_daily_stats(day_cmp, month_cmp, year1_cmp, year2_cmp),
        }
        return render(request, self.template_name, context)
