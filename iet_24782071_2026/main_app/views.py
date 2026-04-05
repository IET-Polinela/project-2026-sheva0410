from django.shortcuts import render, redirect
from .forms import ReportForm
from .models import Report


# READ
def home(request):
    reports = Report.objects.all()
    return render(request, 'main_app/home.html', {'reports': reports})


# CREATE 
def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ReportForm()

    return render(request, 'main_app/create_report.html', {'form': form})


# 🔥 UPDATE (edit data)
def update_report(request, id):
    report = Report.objects.get(id=id)

    if request.method == 'POST':
        form = ReportForm(request.POST, instance=report)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ReportForm(instance=report)

    return render(request, 'main_app/update_report.html', {'form': form})


# 🔥 DELETE (hapus data)
def delete_report(request, id):
    report = Report.objects.get(id=id)
    report.delete()
    return redirect('/')