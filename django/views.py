from django.shortcuts import render,redirect

# Add models, forms, and model forms references here as needed.
from ||app||.models import ||model||
from ||app||.forms import ||model||Form

# template variables.
# app, model, model_instance, redirect_routine_name, render_url

# Create your views here.
def create_account(request):
    if request.method == 'POST':
        form_||model_instance|| = ||model_instance | capitalize||Form(request.POST or None)

        if form_||model_instance||.is_valid()
            ||model_instance||.save()

            return redirect('||redirect_route_name||')
    else:
        form_||model_instance|| = ||model||Form()

    context = {
        'form_||model_instance||' : form_||model_instance||
    }

    return render(request, '||render_url||', context)
