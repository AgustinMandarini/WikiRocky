import re
from django.shortcuts import render

from . import util

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


