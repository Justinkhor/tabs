from django.urls import path
from . import views
from chords import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name = 'signup'),
    path('login', views.login_view, name = 'login'),
    path('logout', views.logout_view, name = 'logout'),
    path('error', views.error_view, name = 'error'),
    path('search_results', views.search_results, name='search_results'),
    path('recent', views.recently_viewed, name='recently_viewed'),
    path('new', views.sheet_new, name='sheet_new'),
    path('<int:pk>', views.sheet_detail, name='sheet_detail'),
    path('<int:pk>/edit', views.sheet_edit, name='sheet_edit'),
    path('playlist', views.playlist, name='playlist'),
    path('playlist_new', views.playlist_new, name='playlist_new'),
    path('playlist/<int:pk>', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:pk>/edit', views.playlist_edit, name='playlist_edit'),
    path('playlist_add/<int:pk>', views.playlist_add, name='playlist_add'),
    path('playlist_remove/<int:pk>', views.playlist_remove, name='playlist_remove'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
