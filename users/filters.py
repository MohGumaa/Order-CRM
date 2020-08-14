import django_filters
from django_filters import DateFilter, CharFilter
from .models import Order

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(label="From", field_name="dated_created", lookup_expr='gte')
    end_date = DateFilter(label="To", field_name="dated_created", lookup_expr='lte')
    note = CharFilter(field_name="note", lookup_expr='icontains')
    class Meta:
        model = Order
        fields = ['product', 'status', 'note', 'start_date', 'end_date']
        # exclude = ['customer', 'dated_created']
