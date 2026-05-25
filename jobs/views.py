from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Job, TeamMember, PlantItem, Vehicle


def operative_form(request):
    plant_choices = PlantItem.PLANT_NAMES
    plant_costs = PlantItem.COSTS
    vehicle_types = Vehicle.VEHICLE_TYPES

    if request.method == 'POST':
        works_order_ref = request.POST.get('works_order_ref', '').strip()
        operative_name = request.POST.get('operative_name', '').strip()
        arrived_time = request.POST.get('arrived_time')
        departed_time = request.POST.get('departed_time')
        notes = request.POST.get('notes', '').strip()

        if not works_order_ref or not operative_name or not arrived_time or not departed_time:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'jobs/operative_form.html', {
                'plant_choices': plant_choices,
                'plant_costs': plant_costs,
                'vehicle_types': vehicle_types,
            })

        job = Job.objects.create(
            works_order_ref=works_order_ref,
            operative_name=operative_name,
            arrived_time=arrived_time,
            departed_time=departed_time,
            notes=notes,
        )

        # Save team members
        team_names = request.POST.getlist('team_members')
        for name in team_names:
            if name.strip():
                TeamMember.objects.create(job=job, name=name.strip())

        # Save plant items
        plant_items = request.POST.getlist('plant_items')
        for item_key in plant_items:
            if item_key:
                PlantItem.objects.create(job=job, item_key=item_key)

        # Save vehicles
        v_types = request.POST.getlist('vehicle_type')
        v_regs = request.POST.getlist('vehicle_reg')
        v_times = request.POST.getlist('vehicle_arrived')
        for vt, vr, va in zip(v_types, v_regs, v_times):
            if vr.strip() and va:
                Vehicle.objects.create(
                    job=job,
                    vehicle_type=vt,
                    registration=vr.strip().upper(),
                    arrived_time=va,
                )

        messages.success(request, f'Job {job.works_order_ref} submitted successfully!')
        return redirect('job_success', job_id=job.id)

    return render(request, 'jobs/operative_form.html', {
        'plant_choices': plant_choices,
        'plant_costs': plant_costs,
        'vehicle_types': vehicle_types,
    })


def job_success(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'jobs/job_success.html', {'job': job})


def qs_dashboard(request):
    jobs = Job.objects.all().order_by('-submitted_at')
    total_all_jobs = sum(j.total_cost() for j in jobs)
    return render(request, 'jobs/qs_dashboard.html', {
        'jobs': jobs,
        'total_all_jobs': total_all_jobs,
    })


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    team = job.teammember_set.all()
    plant = job.plantitem_set.all()
    vehicles = job.vehicle_set.all()
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'team': team,
        'plant': plant,
        'vehicles': vehicles,
    })
