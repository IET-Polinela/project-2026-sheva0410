from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Report


class ReportListView(ListView):
    model = Report
    template_name = 'main_app/home.html'
    context_object_name = 'reports'


class ReportDetailView(DetailView):
    model = Report
    template_name = 'main_app/detail.html'


class ReportCreateView(CreateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/create_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil ditambahkan!")
        return super().form_valid(form)


class ReportUpdateView(UpdateView):
    model = Report
    fields = ['title', 'category', 'description', 'location']
    template_name = 'main_app/update_report.html'
    success_url = reverse_lazy('report_list')

    def form_valid(self, form):
        messages.success(self.request, "Laporan berhasil diperbarui!")
        return super().form_valid(form)


class ReportDeleteView(DeleteView):
    model = Report
    template_name = 'main_app/delete_report.html'
    success_url = reverse_lazy('report_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Laporan berhasil dihapus!")
        return super().delete(request, *args, **kwargs)


class ReportUpdateStatusView(View):
    def post(self, request, pk):
        report = get_object_or_404(Report, pk=pk)
        report.status = request.POST.get('status')
        report.save()
        messages.success(request, "Status berhasil diubah!")
        return redirect('report_list')