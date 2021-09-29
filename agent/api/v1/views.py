from rest_framework.generics import get_object_or_404, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from agent.api.v1.serializers import AgentSerializer, DSOSerializer
from agent.models import Agent, DSO
from core.api.permissions import IsObjectOwner, IsSuperUser
from core.utils import get_logger

logger = get_logger()


class DSOListCreateAPIView(ListCreateAPIView):
    serializer_class = DSOSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = DSO.objects.all()


class DSOItemAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DSOSerializer
    permission_classes = [IsAuthenticated, IsSuperUser]

    def get_object(self):
        dso_id = self.request.query_params.get('id')
        return get_object_or_404(DSO, id=dso_id)


class AgentListCreateAPIView(ListCreateAPIView):
    serializer_class = AgentSerializer
    queryset = Agent.objects.all()
    permission_classes = [IsAuthenticated]
    filterset_fields = ['dso', 'qr_string', 'agent_type', 'status', 'reg_capability', 'reg_date']
    search_fields = ['geo_code']


class AgentItemAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AgentSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

    def get_object(self):
        agent_id = self.request.query_params.get('id')
        return get_object_or_404(Agent, id=agent_id)
