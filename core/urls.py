from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('sn.urls')),#sistema de gerenciamento de certificados
    path('', include('login.urls')),#sitenma de gerenciamento de força, posto, quadro

    path('admin/', admin.site.urls),
    

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = 'sn.views.handler404'  # substitua 'myapp' pelo nome do seu aplicativo
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path('__debug__/', include(debug_toolbar.urls)),
#     ] + urlpatterns
