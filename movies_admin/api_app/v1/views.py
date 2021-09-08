from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import F, Subquery, OuterRef
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from main_app.models import Film, PersonsFilms


class MoviesAPIMixin:
    model = Film
    http_method_names = ('get', )

    def get_queryset(self):
        values = ('id', 'title', 'creation_date', 'rating', 'type')
        all_persons = PersonsFilms.objects.filter(movie=OuterRef('id'))
        actors = all_persons.filter(part=PersonsFilms.PersonRole.ACTOR)
        writers = all_persons.filter(part=PersonsFilms.PersonRole.WRITER)
        directors = all_persons.filter(part=PersonsFilms.PersonRole.DIRECTOR)

        object_list = super().get_queryset().values(*values).annotate(
            description=F('plot'),
            genres=ArrayAgg(F('genre_set__name'), distinct=True),
            actors=ArrayAgg(Subquery(actors.values('person__name')[:1]), distinct=True),
            writers=ArrayAgg(Subquery(writers.values('person__name')[:1]), distinct=True),
            directors=ArrayAgg(Subquery(directors.values('person__name')[:1]), distinct=True)
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
