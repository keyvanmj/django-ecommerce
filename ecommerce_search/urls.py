from django.urls import path
from .views import Result,JSONView
urlpatterns = [
    path('results',Result.as_view(),name='search_results'),
    path('result',JSONView.as_view(),name='live_search'),

]

