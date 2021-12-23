import re
import os
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from random import randint


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None

def edit_file(title, page_content):
    """
    Implemented it before knowing there was already a "save_entry"
    function that does the same thing. At least I made some practice 
    on building and implementing my own functions.
    """
    new_page_path = os.path.join(settings.BASE_DIR, f'entries/{title}.md')
    with open(new_page_path, 'w', encoding="utf-8") as file:
        file.write(f'{page_content}')
    try:
        if title not in list_entries():
            os.remove(os.path.join(settings.BASE_DIR, f'entries/{title}.md'))
    except OSError:
        return None

def read_file(title):
    """

    Same as "edit_file", I implemented this before knowing there were 
    functions less verbose than mine already written
    """
    edit_page_path = os.path.join(settings.BASE_DIR, f'entries/{title}.md')
    with open(edit_page_path, 'r', encoding="utf-8") as file:
        file_content = file.read()
    page_title = title
    page_content = file_content

    return page_content

def random_title():

    n = randint(0, len(list_entries())-1)
    return list_entries()[n]