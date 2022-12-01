from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.db.models import Q
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required

from .models import Topic, Entry
from .forms import TopicForm, EntryForm

# Create your views here.

def index(request):
    """Load the index page"""
    topics = Topic.objects.order_by('-created_time')
    newest_topics = topics[0:3]

    context = {'newest_topics': newest_topics}

    return render(request, 'pedia/index.html', context)

def topics(request):
    """Load the topics page"""

    topics = Topic.objects.order_by("title")

    context = {'topics': topics}

    return render(request, 'pedia/topics.html', context)
    
@login_required
def topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by("title")
    context = {'topic': topic, 'entries': entries}
    return render(request, 'pedia/topic.html', context)

@login_required
def add_topic(request):

    if request.method != 'POST':
    # no data submitted
        form = TopicForm()
    
    else:
    # data submitted
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pedia:topics'))

    context = {'form': form}    
    return render(request, 'pedia/add_topic.html', context)

@login_required
def add_entry(request, topic_id):

    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
    # no data submitted
        form = EntryForm()
    
    else:
    # data submitted
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('pedia:topic', args=[topic_id]))
    
    context = {'topic': topic, 'form': form}
    return render(request, 'pedia/add_entry.html', context)

@login_required
def edit_entry(request, entry_id):

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
   
    if request.method != 'POST':
    # no data submitted
        form = EntryForm(instance=entry)
    
    else:
    # data submitted
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('pedia:topic', args=[topic.id]))

    context = {'entry': entry, 'form': form, 'topic': topic}
    return render(request, 'pedia/edit_entry.html', context)

def delete_entry(request, entry_id):
    """Delete an entry"""
    
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if entry.owner == request.user:
        entry.delete()
    
    return HttpResponseRedirect(reverse('pedia:topic', args=[topic.id]))


class SearchResultsView(ListView):
    """Load a search result page"""
    model = Topic
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Topic.objects.filter(
                        Q(title__icontains=query) | Q(description__icontains=query) 
                    )
        return object_list

    