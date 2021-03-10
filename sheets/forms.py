from django import forms
from .models import Sheet, Playlist

class SheetForm(forms.Form):
    title = forms.CharField(max_length = 200)
    artist = forms.CharField(max_length=200)
    key = forms.CharField(max_length = 2)
    file = forms.FileField()

class SheetEditForm(forms.ModelForm):
    class Meta:
        model = Sheet
        fields = ('title', 'artist', 'key', 'chords',)
        widgets = {'chords': forms.Textarea(attrs={'rows':30, 'cols':50}),}

class PlaylistForm(forms.Form):
    playlist_name = forms.CharField(max_length = 50)
    # sheets = forms.ModelMultipleChoiceField(widget = forms.CheckboxSelectMultiple, queryset = Sheet.objects.all())

class PlaylistEditForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ('playlist_name',)
