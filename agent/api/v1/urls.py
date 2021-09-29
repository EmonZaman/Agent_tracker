from django.urls import path

from agent.api.v1.views import AgentItemAPIView, AgentListCreateAPIView, DSOItemAPIView, DSOListCreateAPIView

app_name = 'agent-api-v1'
urlpatterns = [
    path('dso/', DSOListCreateAPIView.as_view(), name='ma-list-create'),
    path('dso/item/', DSOItemAPIView.as_view(), name='ma-item'),

    path('agents/', AgentListCreateAPIView.as_view(), name='agent-list-create'),
    path('agents/item/', AgentItemAPIView.as_view(), name='agent-item'),
]
