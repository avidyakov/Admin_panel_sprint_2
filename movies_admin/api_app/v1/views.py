from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from main_app.models import Film, PersonsFilms


class MoviesAPIMixin:
    model = Film
    http_method_names = ('get', )

    def get_queryset(self):
        values = ('id', 'title', 'plot', 'creation_date', 'rating', 'type')
        object_list = super().get_queryset().values(*values).annotate(
            genres=ArrayAgg(F('genre_set__name'), distinct=True),
            actors=ArrayAgg(PersonsFilms.objects.filter(movie=F('id'), part='a').values('person__id'), distinct=True),
            directors=ArrayAgg(PersonsFilms.objects.filter(movie=F('id'), part='d').values('person__id'), distinct=True),
            writers=ArrayAgg(PersonsFilms.objects.filter(movie=F('id'), part='w').values('person__id'), distinct=True),
        )
        return object_list

    def render_to_response(self, context):
        return JsonResponse(context)


class Movies(MoviesAPIMixin, BaseListView):
    page_count = 20

    def get_context_data(self, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, _ = self.paginate_queryset(queryset, self.page_count)
        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset)
        }
        return context


class MovieDetail(MoviesAPIMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.pop('view')
        return context
