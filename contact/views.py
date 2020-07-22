from django.shortcuts import render, reverse, HttpResponseRedirect
from contact.models import Contact
from contact.forms import ContactForm


def AddContactView(request):
    html = "form.html"
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Contact.objects.create(
                subject=data['subject'],
                message=data['message'],
                sender=data['email'],
                cc_myself=data['ccc'],
            )
        return HttpResponseRedirect(reverse('home'))
    form = ContactForm()
    return render(request, html, {'form': form})
