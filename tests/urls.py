from django.urls import path
from .views import VariantListView, QuestionFilterView
urlpatterns = [
    path('variants/', VariantListView.as_view(), name='variant-list'),
    path('questions/filter/', QuestionFilterView.as_view(), name='question-filter'),
]