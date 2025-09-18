from django.db.models import Q
from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {'emps': emps}
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            salary = int(request.POST.get('salary', 0))
            bonus = int(request.POST.get('bonus', 0))
            phone = int(request.POST.get('phone', 0))
            dept = int(request.POST.get('department'))
            role = int(request.POST.get('role'))

            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                phone=phone,
                bonus=bonus,        # 👈 bonus_id mat likho, agar bonus IntegerField hai
                dept_id=dept,       # 👈 dept ForeignKey hai to _id chalega
                role_id=role,       # 👈 role ForeignKey hai to _id chalega
                hire_date=datetime.now()
            )
            new_emp.save()
            return HttpResponse("Employee added successfully ✅")

        except Exception as e:
            return HttpResponse(f"Error: {e}")

    elif request.method == 'GET':
        return render(request, 'add_emp.html')

    else:
        return HttpResponse("Invalid request method")

def remove_emp(request,emp_id=0):

    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(pk=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee removed successfully")
        except:
            return HttpResponse("PLZZ Enter A Valid Employee ID")
    emps = Employee.objects.all()
    context = {'emps': emps}
    return render (request,'remove_emp.html', context)


from django.shortcuts import render, HttpResponse
from .models import Employee, Department, Role
from django.db.models import Q

def filter_emp(request):
    emps = Employee.objects.all()  # Default: sab employees

    if request.method == 'POST':
        name = request.POST.get('name')
        dept = request.POST.get('dept')
        role = request.POST.get('role')

        if name:
            emps = emps.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
        if dept:
            emps = emps.filter(dept__name=dept)
        if role:
            emps = emps.filter(role__name=role)

        context = {'emps': emps}
        return render(request, 'view_all_emp.html', context)

    # Agar GET request hai
    elif request.method == 'GET':
        depts = Department.objects.all()
        roles = Role.objects.all()
        context = {'depts': depts, 'roles': roles}
        return render(request, 'filter_emp.html', context)

    else:
        return HttpResponse("Invalid request method")