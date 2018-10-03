from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.utils.translation import gettext as _

from appgu.forms import ContactForm
from ..models import Vehicles, NewsPosts, Vehicles_Tuscany, NewsPosts_Tuscany
from django.template.loader import get_template
from .. import forms

# Tuscany index (homepage)
def index(request):
    vehicle_list = Vehicles_Tuscany.objects.all()
    if len(vehicle_list) != 0:
        # the c_type determines what style class each vehicle item gets
        c_type = 0

        if len(vehicle_list) % 3 == 1:
            c_type = 1
        elif len(vehicle_list) % 3 == 2:
            c_type = 2

        last = Vehicles_Tuscany.objects.latest('id')
        if len(vehicle_list) > 1:
            secondlast = vehicle_list.order_by('-id')[1]
        else:
            secondlast = ''
        paginator = Paginator(vehicle_list, 9)  # Show 9 contacts per page

        page = request.GET.get('page')
        vehicles = paginator.get_page(page)
        return render(request, 'tuscany/index.html', {'vehicles': vehicles, 'c_type': c_type, 'last': last, 'secondlast': secondlast, 'exists': True})
    return render(request, 'tuscany/index.html', {'exists': False})

# dealers page
def dealers(request):
    return render(request, 'tuscany/dealers.html')

# events page
def events(request):
    return render(request, 'tuscany/events.html')

# shop page
def shop(request):
    return render(request, 'tuscany/contact.html')

# news page
def news(request):
    if request.method == 'GET' and 'n' in request.GET:
        n = request.GET['n']
        if n is not None and n != '':
            news_list = NewsPosts_Tuscany.objects.filter(pk=request.GET.get('n'))
            if len(news_list) == 0:
                exists = False
            else:
                exists = True
            return render(request, 'tuscany/news.html', {'newsposts': news_list, 'exists': exists, 'news': NewsPosts_Tuscany.objects.order_by('-date'), 'singlepost': True})
    else:
        news_list = NewsPosts_Tuscany.objects.order_by('-date')[:30]
        if len(news_list) == 0:
            exists = False
        else:
            exists = True
        paginator = Paginator(news_list, 1)  # Show 1 newspost per page
        page = request.GET.get('page')
        newsposts = paginator.get_page(page)
        return render(request, 'tuscany/news.html', {'newsposts': newsposts, 'exists': exists, 'news': news_list})

    if not news:
        return render(request, 'tuscany/news.html', {"exists": False})
    l = []
    for i in news:
        l.append(i.banner)
        l.append(i.title)
        l.append(i.headline)
        l.append(i.description)
        l.append(i.quote)
        l.append(i.quotefooter)
        l.append(i.date)
        l.append(i.writtenby)

    return render(request, 'shelby/news.html',
                  {'banner': l[0], 'title': l[1], 'headline': l[2], 'desc': l[3], 'quote': l[4], 'quotefooter': l[5], 'date': l[6], 'writtenby': l[7], 'exists': True})

# press and media page
def pressandmedia(request):
    return render(request, 'tuscany/media.html')


# contact page
def contact(request):
    form_class = forms.ContactForm(auto_id=False)

    if request.method == 'POST':
        form = forms.ContactForm(request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
                , '')
            contact_email = request.POST.get(
                'contact_email'
                , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('tuscany/contact_template.txt')
        context = {
            'contact_name': contact_name,
            'contact_email': contact_email,
            'form_content': form_content,
        }
        content = template.render(context)

        email = EmailMessage(
            "New contact form submission",
            content,
            "Tuscany" + '',
            ['selimaydi@gmail.com'],
            headers={'Reply-To': contact_email}
        )
        email.send()
        return redirect('tuscany_contact')

    return render(request, 'tuscany/contact.html', {
        'form': form_class,
    })

# description page for a particular vehicle
def vehicledesc(request):
    if request.method == "GET" and 'v' in request.GET:
        v = request.GET['v']
        if v is not None and v != '':
            vehicles = Vehicles_Tuscany.objects.filter(pk=request.GET.get('v'))
            if not vehicles:
                return render(request, 'tuscany/vehicledesc.html', {"exists": False})
            l = []
            for i in vehicles:
                l.append(i.image)
                l.append(i.model)
                l.append(i.headline)
                l.append(i.description)

            return render(request, 'tuscany/vehicledesc.html', {'image': l[0], 'model': l[1], 'headline': l[2], 'desc': l[3], 'exists': True})
    else:
        return render(request, 'tuscany/vehicledesc.html')