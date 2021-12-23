import re
import markdown2
from django import forms
from django.shortcuts import render 
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from . import util


class NewPage(forms.Form):
	title = forms.CharField(label="Title", max_length=100)
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

	page_content = markdown2.markdown(util.get_entry(title))

	return render(request, "encyclopedia/title.html", {
		"page_content": page_content, "title": title
	})

def new_page(request):
	if request.method == "POST":
		form = NewPage(request.POST)
		if form.is_valid():
			title = form.cleaned_data["title"]
			page_content = form.cleaned_data["page_content"]
			if title in util.list_entries():
				alert = True
				return render(request, "encyclopedia/new_page.html", {
					"form":form, "alert":alert
					})

			util.edit_file(title, page_content)

			return HttpResponseRedirect(reverse("encyclopedia:title", args=[title]))	
	else:
		return render(request, "encyclopedia/new_page.html", {
			"form":NewPage(), "templ_name": "New Page"
		})

def edit_page(request, title):
	if request.method == "POST":
		title = request.POST.get("title")
		form = NewPage(request.POST)

		if form.is_valid():
			page_content = form.cleaned_data["page_content"]
			util.edit_file(title, page_content)
			
			return HttpResponseRedirect(reverse("encyclopedia:title", args=[title]))
	else:
		page_content = util.read_file(title)
		form = NewPage({"title": title, "page_content": page_content})

		return render(request, "encyclopedia/edit_page.html", {
			"form":form, "templ_name": "Edit Page"
			})

def random_page(request):
	page_title = util.random_title()
	return HttpResponseRedirect(reverse("encyclopedia:title", args=[page_title]))