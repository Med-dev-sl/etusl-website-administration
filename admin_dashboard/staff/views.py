from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Leadership
from .forms import LeadershipForm


@login_required
def edit_my_leadership(request):
	# Find Leadership linked to the logged-in user
	leadership = get_object_or_404(Leadership, user=request.user)

	if request.method == 'POST':
		form = LeadershipForm(request.POST, request.FILES, instance=leadership)
		if form.is_valid():
			form.save()
			return redirect('staff:leadership_detail')
	else:
		form = LeadershipForm(instance=leadership)

	return render(request, 'staff/edit_leadership.html', {'form': form, 'leadership': leadership})


@login_required
def leadership_detail(request):
	leadership = get_object_or_404(Leadership, user=request.user)
	return render(request, 'staff/leadership_detail.html', {'leadership': leadership})
