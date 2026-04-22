from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Report


class ReportListView(LoginRequiredMixin, ListView):
    model = Report
    template_name = 'main_app/reports.html'
    context_object_name = 'reports'


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

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


# UPDATE STATUS (DENGAN WORKFLOW AMAN)
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