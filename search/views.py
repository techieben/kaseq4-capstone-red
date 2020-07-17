# views.py

# https://www.calazan.com/how-to-add-full-text-search-to-your-django-app-with-a-postgresql-backend/

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.views.generic import ListView

from recipe.models import Recipe


class SearchListView(ListView):
    """
    Display a Recipe List page filtered by the search query.
    """
    template_name = 'search.html'
    model = Recipe
    paginate_by = 10

    def get_queryset(self):
        qs = Recipe.objects.all()

        keywords = self.request.GET.get('q')
        if keywords:
            query = SearchQuery(keywords)
            title_vector = SearchVector('title', weight='A')
            description_vector = SearchVector('description', weight='B')
            instructions_vector = SearchVector('instructions', weight='C')
            vectors = title_vector + description_vector + instructions_vector
            qs = qs.annotate(search=vectors).filter(search=query)
            qs = qs.annotate(rank=SearchRank(vectors, query)).order_by('-rank')

        return qs
