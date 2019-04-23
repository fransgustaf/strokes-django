from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/document/', views.DocumentList.as_view()),
    path('api/document/<int:document_pk>/', views.DocumentDetails.as_view()),
#    path(r'^api/document/(?P<pk>\d+)/', views.Document.as_view()),
    path('api/document/<int:document_pk>/page/', views.DocumentPageList.as_view()),
    path('api/page/<int:page_pk>/', views.PageDetails.as_view()),
    path('api/page/<int:page_pk>/stroke/', views.PageStrokeList.as_view()),

    path('api/page/<int:page_pk>/field/', views.PageFieldList.as_view()),

]
