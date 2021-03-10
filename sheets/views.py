from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.utils import timezone
from .models import Sheet, Playlist
from .forms import SheetForm, PlaylistForm, SheetEditForm, PlaylistEditForm

def home(request):
    sheets = Sheet.objects.order_by('-created_date')[:10]
    return render(request, 'sheets/home.html', {'sheets': sheets})

def error_view(request):
    return render(request, 'sheets/error.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'sheets/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return redirect('error')
    return render(request, 'sheets/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

recent = []
@login_required
def sheet_detail(request, pk):
    sheet = get_object_or_404(Sheet, pk=pk)
    added_to_playlist = False

    if sheet in recent:
        recent.remove(sheet)
    recent.append(sheet)

    if len(Playlist.objects.filter(user=request.user)) > 0:
        playlist = Playlist.objects.filter(user=request.user).order_by('-created_date')[0]

        if sheet in playlist.sheets.all():
            added_to_playlist = True

    sheets = Sheet.objects.filter(Q(title=sheet.title) | Q(artist=sheet.artist))
    return render(request, 'sheets/sheet_detail.html', {'sheet': sheet, 'sheets':sheets, 'added_to_playlist': added_to_playlist})

@login_required
def sheet_new(request):
    if request.method == 'POST':
        form = SheetForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.cleaned_data
            file = request.FILES['file']
            file_type = str(file).split('.')[-1].lower()
            if file_type != 'txt':
                return render(request, 'sheets/error.html')
            string = file.read().decode()
            sheet = Sheet(title = form['title'], artist = form['artist'], key = form['key'], chords = string)
            sheet.save()
            return redirect('sheet_detail', pk=sheet.pk)
    else:
        form = SheetForm()
    return render(request, 'sheets/sheet_edit.html', {'form': form})

@login_required
def sheet_edit(request, pk):
    sheet = get_object_or_404(Sheet, pk=pk)
    if request.method == "POST":
        form = SheetEditForm(request.POST, instance=sheet)
        if form.is_valid():
            sheet = form.save(commit=False)
            sheet.save()
            return redirect('sheet_detail', pk=sheet.pk)
    else:
        form = SheetEditForm(instance=sheet)
    return render(request, 'sheets/sheet_edit.html', {'form': form})

@login_required
def playlist_add(request, pk):
    sheet = get_object_or_404(Sheet, pk=pk)
    if len(Playlist.objects.filter(user=request.user)) == 0:
        return render(request, 'sheets/playlist_error.html')
    playlist = Playlist.objects.filter(user=request.user).order_by('-created_date')[0]
    playlist.sheets.add(sheet)
    playlist.save()
    return redirect('playlist_detail', pk=playlist.pk)

@login_required
def playlist_remove(request, pk):
    sheet = get_object_or_404(Sheet, pk=pk)
    playlist = Playlist.objects.filter(user=request.user).order_by('-created_date')[0]
    playlist.sheets.remove(sheet)
    playlist.save()
    return redirect('playlist_detail', pk=playlist.pk)

@login_required
def playlist(request):
    playlists = Playlist.objects.order_by('-created_date')[:10]
    return render(request, 'sheets/playlist.html', {'playlists': playlists})

@login_required
def playlist_detail(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    return render(request, 'sheets/playlist_detail.html', {'playlist': playlist})

@login_required
def playlist_new(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            playlist = Playlist(user = request.user, playlist_name = form['playlist_name'])
            playlist.save()
            return redirect('playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistForm()
    return render(request, 'sheets/playlist_edit.html', {'form': form})

@login_required
def playlist_edit(request, pk):
    playlist = get_object_or_404(Playlist, pk=pk)
    if request.method == "POST":
        form = PlaylistEditForm(request.POST)
        if form.is_valid():
            playlist = form.save(commit=False)
            playlist.save()
            return redirect('playlist_detail', pk=playlist.pk)
    else:
        form = PlaylistEditForm(instance=playlist)
    return render(request, 'sheets/playlist_edit.html', {'form': form})

@login_required
def search_results(request):
    query = request.GET['q']
    sheets = Sheet.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))
    return render(request, 'sheets/results.html', {'sheets': sheets})

@login_required
def recently_viewed(request):
    sheets = recent
    return render(request, 'sheets/recent.html', {'sheets': sheets})
