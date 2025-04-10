from django.urls import path
from .views import VariantListView, QuestionFilterView, ExportTestResultsToExcel
urlpatterns = [
    path('variants/', VariantListView.as_view(), name='variant-list'),
    path('questions/filter/', QuestionFilterView.as_view(), name='question-filter'),
    path('excel-import/', ExportTestResultsToExcel.as_view(), name='excel-import'),
]
