from django.shortcuts import render

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
	if util.get_entry(title) == None:
		return render(request, "encyclopedia/404.html")
	return render(request, "encyclopedia/title.html", {
		"title": util.get_entry(title), "page_title": title
	})

def search(request):
	if request.method == "POST":
		return render(request, "encyclopedia/search.html")
