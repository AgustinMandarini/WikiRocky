import re
import os
from django import forms
from django.shortcuts import render 
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings

from . import util


class NewPage(forms.Form):
	page_title = forms.CharField(label="Title", max_length=100)
	page_content = forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
	q = request.GET["q"]
	r = re.compile(q, re.IGNORECASE)
	title = util.list_entries()
	result = list(filter(r.findall, title))
	return render(request, "encyclopedia/search.html", {
		"q": q, "result": result
	})

def title(request, title):
	if util.get_entry(title) == None:
		return render(request, "encyclopedia/404.html")
	return render(request, "encyclopedia/title.html", {
		"title": util.get_entry(title), "page_title": title
	})

def new_page(request):
	if request.method == "POST":
		form = NewPage(request.POST)
		if form.is_valid():
			page_title = form.cleaned_data["page_title"]
			page_content = form.cleaned_data["page_content"]
			if page_title in util.list_entries():
				alert = True
				return render(request, "encyclopedia/new_page.html", {
					"form":form, "alert":alert
					})
			new_page_path = os.path.join(settings.BASE_DIR, f'entries/{page_title}.md')
			with open(new_page_path, 'w', encoding="utf-8") as file:
				file.write(f'#{page_title}\n\n{page_content}')
			return HttpResponseRedirect(reverse("encyclopedia:title", args=[page_title]))	
	else:
		return render(request, "encyclopedia/new_page.html", {
			"form":NewPage()
		})


def edit_page(request, title):
	print(request.GET)
	#title = request.GET["title"]
	#form = NewPage(util.list_entries()[title])
	#print(form)
	return HttpResponse("<h1>OK</h1>")