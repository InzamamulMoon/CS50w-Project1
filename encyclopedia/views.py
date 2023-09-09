from typing import Any, Mapping, Optional, Type, Union
from django.forms.utils import ErrorList
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse
from django import forms
from . import util
import markdown2
import random

class EditForm(forms.Form):
    edit_entry=forms.CharField(widget=forms.Textarea)

class EntryForm(forms.Form):
   title=forms.CharField(label="Enter title")
   new_entry=forms.CharField(widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        
    })

def entry_page(request, title):
           
     if util.get_entry(title)==None:
        return render(request, "encyclopedia/Error.html",{
        })
     else:
        entry=util.get_entry(title)
        return render(request, "encyclopedia/Entry_page.html",{
        "page":markdown2.markdown(entry),
        "title":title
        })

def search(request): 
   if request.method=="GET":
    item=request.GET['q']
    q=item.lower()
    list_entries=util.list_entries()
    entries=[]
    for entry in list_entries:
     new_entry=entry.lower()
     if q in new_entry:
      if q==new_entry:
       page=util.get_entry(item)
       return render(request, "encyclopedia/Entry_page.html",{
                "page":markdown2.markdown(page),
                "title": item})
      else:
           entries.append(entry)
    return render(request, "encyclopedia/Searh_results.html",{
          "entries": entries
    })
def new_page(request):
    if request.method=="POST":
        form= EntryForm(request.POST)
        title=request.POST['title']
        new_entry=request.POST['new_entry']
        if form.is_valid():
             entry=util.get_entry(title)
             if entry!=None:
                return render(request, "encyclopedia/Error.html")
             else:
                util.save_entry(title,new_entry)
                entry=util.get_entry(title)
                return render(request, "encyclopedia/Entry_page.html",{
                "page":markdown2.markdown(entry),
                "title":title
                })
    return render(request, "encyclopedia/New_page.html",{
    "form":EntryForm()
    })

def random_page(request):
    entries=util.list_entries()
    title=random.choice(entries)
    return redirect(reverse('entry_page', args=[title]))

#Make new class similar to Entry form, and have it reutrn to the entry page 
def edit_page(request,title):
    page=util.get_entry(title)
    if title==None:
        return render(request, "encyclopedia/Error.html")
    if request.method=="POST":
        edit=EditForm(request.POST)
        if edit.is_valid():
            edit=edit.cleaned_data['edit_entry']
            util.save_entry(title,edit)
            return redirect(reverse('entry_page', args=[title]))
    return render(request, "encyclopedia/Edit_page.html",{
         "title": title,
         "edit_entry": EditForm(initial={"edit_entry":page})
    })