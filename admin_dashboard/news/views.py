from rest_framework import viewsets
from .models import NewsPost
from .serializers import NewsPostSerializer


class NewsPostViewSet(viewsets.ModelViewSet):
    queryset = NewsPost.objects.all().order_by('-published_at')
    serializer_class = NewsPostSerializer
