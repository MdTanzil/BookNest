from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('add/<int:book_id>/', views.review_add, name='review_add'),
    path('update/<int:review_id>/', views.review_update, name='review_update'),
    path('delete/<int:review_id>/', views.review_delete, name='review_delete'),
]
