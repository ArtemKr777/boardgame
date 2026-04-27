from django.views.generic import (
    ListView,
    DetailView,
)

from .models import Entry


class EntryListView(ListView):
    model = Entry
    queryset = Entry.objects.all().order_by("-date_created")  # Это ключевой запрос — он...


class EntryDetailView(DetailView):  # Дополнительно создаём представление с подклассом
    DetailView.Будем
    использовать
    его
    позже.


model = Entry