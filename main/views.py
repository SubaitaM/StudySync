from django.shortcuts import render, redirect, get_object_or_404
from .models import Event

def signup(request):
    return render(request, "SignUp.html")

def upload_doc(request):
    return render(request, "UploadDoc.html")  # Upload Document page

def loading(request):
    return render(request, "Loading.html")  # Loading page

def list_events(request):
    # Handle creation if POST
    if request.method == 'POST':
        event = request.POST.get('event')
        subject = request.POST.get('subject')
        due_date = request.POST.get('due_date')
        if subject and due_date:
            Event.objects.create(events=events,subject=subject, due_date=due_date)
        return redirect('list_events')  # reload the page

    # Otherwise, just show the events
    events = Event.objects.all()
    return render(request, 'list_events.html', {"events": events})

def edit_event(request, event_id):
    """
    - GET: Display a form to edit the existing event.
    - POST: Save changes and redirect back to the list.
    """
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        # Grab new data from the form
        event.subject = request.POST.get('subject')
        event.due_date = request.POST.get('due_date')
        event.save()
        return redirect('list_events')  # Go back to the list
    else:
        # GET request: show the edit form
        return render(request, 'edit_event.html', {"event": event})

def delete_event(request, event_id):
    """
    Deletes the event from the database, then redirects to the list.
    """
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    return redirect('list_events')

