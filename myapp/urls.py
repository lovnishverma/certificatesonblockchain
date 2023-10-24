from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),  # Include the admin URLs
    path('save_transaction/<str:certificate_id>/<str:transaction_hash>/', views.save_transaction, name='save_transaction'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('register/', views.registration, name='registration'),
    path('', views.home, name='home'),
    path('privacy_policy/', views.privacy_policy, name='privacy_policy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
