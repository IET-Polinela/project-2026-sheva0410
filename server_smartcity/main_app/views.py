from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Q

from .models import Report


# LIST VIEW
class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/reports.html'
    context_object_name = 'reports'

    def get_queryset(self):
        queryset = Report.objects.all().order_by('-created_at')

        query = self.request.GET.get('q', '').strip()
        status = self.request.GET.get('status', '').strip()
        category = self.request.GET.get('category', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(category__icontains=query)
            )

        if status:
            queryset = queryset.filter(status=status)

        if category:
            queryset = queryset.filter(category=category)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['status_choices'] = Report._meta.get_field('status').choices
        context['category_choices'] = (
            Report.objects.order_by('category')
            .values_list('category', flat=True)
            .distinct()
        )
        context['filters'] = {
            'q': self.request.GET.get('q', '').strip(),
            'status': self.request.GET.get('status', '').strip(),
            'category': self.request.GET.get('category', '').strip(),
        }
        return context


# DETAIL VIEW
class ReportDetailView(LoginRequiredMixin, DetailView):
    model = Report
    template_name = 'main_app/detail.html'


# CREATE
class ReportCreateView(LoginRequiredMixin, CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/create_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses ditolak! Hanya admin yang dapat menambah laporan.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan!")
        return super().form_valid(form)


# UPDATE
class ReportUpdateView(LoginRequiredMixin, UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/update_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses ditolak! Hanya admin yang dapat mengedit.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diperbarui!")
        return super().form_valid(form)


# DELETE
class ReportDeleteView(LoginRequiredMixin, DeleteView):
    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "Akses ditolak! Hanya admin yang dapat menghapus.")
            return redirect('report_list')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        report = self.get_object()
        report.delete()
        messages.success(request, "Laporan berhasil dihapus.")
        return redirect(self.success_url)


# UPDATE STATUS (WORKFLOW)
class ReportUpdateStatusView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_admin:
            messages.error(request, "Akses ditolak! Hanya admin yang dapat mengubah status.")
            return redirect('report_list')

        report = get_object_or_404(Report, pk=pk)

        valid_transitions = {
            'REPORTED': 'VERIFIED',
            'VERIFIED': 'IN_PROGRESS',
            'IN_PROGRESS': 'RESOLVED'
        }

        current = report.status
        new = request.POST.get('status')

        if valid_transitions.get(current) != new:
            messages.error(request, "Transisi status tidak valid!")
            return redirect('report_list')

        report.status = new
        report.save()

        messages.success(request, "Status berhasil diubah!")
        return redirect('report_list')


# LIVE SEARCH (AJAX)
class ReportSearchView(View):
    def get(self, request):
        query = request.GET.get('q', '').strip()
        status = request.GET.get('status', '').strip()
        category = request.GET.get('category', '').strip()

        reports = Report.objects.all().order_by('-created_at')

        if query:
            reports = reports.filter(
                Q(title__icontains=query) |
                Q(location__icontains=query) |
                Q(category__icontains=query)
            )

        if status:
            reports = reports.filter(status=status)

        if category:
            reports = reports.filter(category=category)

        reports = reports.values('id', 'title', 'location', 'status')

        return JsonResponse(list(reports), safe=False)


# DETAIL API (UNTUK MODAL)
class ReportDetailAPIView(View):
    def get(self, request, pk):
        report = get_object_or_404(Report, pk=pk)

        data = {
            'title': report.title,
            'category': report.category,
            'description': report.description,
            'location': report.location,
            'status': report.status,
        }

        return JsonResponse(data)
