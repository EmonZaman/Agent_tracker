from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from agent_tracker.settings import env, MEDIA_ROOT, MEDIA_URL, STATIC_ROOT, STATIC_URL

api_url_patterns = (
    [
        path('accounts/v1/', include('accounts.api.v1.urls')),
        path('agent/v1/', include('agent.api.v1.urls')),
        path('tracker/v1/', include('tracker.api.v1.urls')),
    ], 'api'
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # api
    path('api/', include(api_url_patterns)),
    path('api_auth/', include('rest_framework.urls')),

]

if env.str('ENV_TYPE') == 'DEVELOPMENT':
    import debug_toolbar

    urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
