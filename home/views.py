from django.shortcuts import render
from home.models import AttendanceRecord
from django.core.paginator import Paginator
from datetime import timedelta
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect 

@login_required
def homePage(request):

    if not request.session.get('employee_user_id'):
        return redirect('loginsystem:loginPage') 


    name = request.GET.get('name', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()
    department = request.GET.get('department', '').strip()
    employee_id = request.GET.get('employee_id', '').strip()
    total_time_input = request.GET.get('total_time', '').strip()
    branch = request.GET.get('branch', '').strip()
    results_per_page = request.GET.get('results_per_page', '10')
    page_number = request.GET.get('page', 1)

    # 🔍 Check if any filter is used
    has_search = any([name, date_from, date_to, department, employee_id, total_time_input, branch])

    # ⚙️ Queryset starts either empty or with all records
    records = AttendanceRecord.objects.all() if has_search else AttendanceRecord.objects.none()

    if has_search:
        if name:
            records = records.filter(first_name__icontains=name)
        if employee_id:
            records = records.filter(employee_id=employee_id)
        if department:
            records = records.filter(department__icontains=department)
        if branch:
            records = records.filter(branch__icontains=branch)
        if date_from and date_to:
            records = records.filter(date__range=[date_from, date_to])

        if total_time_input:
            try:
                time_parts = list(map(int, total_time_input.split(":")))
                if len(time_parts) == 1:
                    start = timedelta(hours=time_parts[0])
                    end = timedelta(hours=time_parts[0] + 1)
                elif len(time_parts) == 2:
                    start = timedelta(hours=time_parts[0], minutes=time_parts[1])
                    end = start + timedelta(minutes=1)
                elif len(time_parts) == 3:
                    start = timedelta(hours=time_parts[0], minutes=time_parts[1], seconds=time_parts[2])
                    end = start + timedelta(seconds=1)
                else:
                    raise ValueError("Too many segments in total_time")
                records = records.filter(total_time__gte=start, total_time__lt=end)
            except Exception as e:
                print("⚠️ Invalid total_time input:", total_time_input, "| Error:", e)

    # 📄 Pagination logic
    try:
        results_per_page = int(results_per_page)
    except ValueError:
        results_per_page = 10

    paginator = Paginator(records, results_per_page)
    page_obj = paginator.get_page(page_number)
    total_count = paginator.count

    # 📅 Dropdown data
    departments = [
        'Department', 'ADMIN', 'SUPPORT FUNCTIONS', 'HRD', 'SERVICE',
        'RENTAL', 'PARTS / WAREHOUSE', 'PROJECTS', 'ACCTS',
        'CHENNAI WORKSHOP', 'SALES', 'O & M', '6 SIGMA', 'PSSR',
        'TRAINING', 'ISR SERVICE', 'SYSTEMS', 'SUPPORT FUNCTONS',
        'PROJECT MANAGEMENT', 'MARK COMM', 'ERP', 'PARTS',
        'PROJECT MAINTENANCE', 'MD & CEO OFFICE', 'DIGITAL'
    ]

    branches = ['Bangalore', 'Chennai', 'Hyderabad', 'Mumbai', 'Delhi']  # You can dynamically fetch unique branches from DB if needed

    # 📤 Excel Export
    if request.GET.get('export') == 'xlsx':
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Attendance Records"

        headers = ["Employee ID", "Name", "Department", "Branch", "Date", "First Punch", "Last Punch", "Total Time"]
        ws.append(headers)

        for r in records:
            ws.append([
                r.employee_id,
                r.first_name,
                r.department,
                r.branch,
                r.date.strftime('%Y-%m-%d'),
                r.first_punch,
                r.last_punch,
                str(r.total_time)
            ])

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=attendance_records.xlsx'
        wb.save(response)
        return response

    return render(request, 'home/home.html', {
        'records': page_obj.object_list,
        'page_obj': page_obj,
        'has_search': has_search,
        'name': name,
        'date_from': date_from,
        'date_to': date_to,
        'department': department,
        'employee_id': employee_id,
        'total_time': total_time_input,
        'results_per_page': results_per_page,
        'total_count': total_count,
        'departments': departments,
        'branch': branch,
        'branches': branches,
    })
