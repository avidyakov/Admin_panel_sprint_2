from django.http import JsonResponse
from django.views.generic.list import BaseListView

from main_app.models import Film


class MoviesAPIMixin:
    model = Film
    http_method_names = ('get', )

    def get_queryset(self):
        values = (
            'id', 'title', 'plot', 'creation_date',
            'rating', 'type', 'genres__name', 'persons__name'
        )
        object_list = Film.objects.all().prefetch_related('persons', 'genres').values(*values)
        return list(object_list)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.pop('view')
        return context

    def render_to_response(self, context):
        return JsonResponse(context)


class Movies(MoviesAPIMixin, BaseListView):
    pass
