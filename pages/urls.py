# pages/urls.py
from django.urls import path
from .views import HomePageView, AboutPageView, ColumnsView, ExtractMetadataView, CleanMetadataView, FindColVisView, FindFileResultsView, ListMethodsView, RunMethodView # , CreateFileDistView, CreateNetworkView, CreateVisColumnView

urlpatterns = [
    path('about/', AboutPageView.as_view(), name='about'),
    path('', HomePageView.as_view(), name='home'),
    path('methods/list',ListMethodsView.as_view(),name='list_methods'),
    path('runmethod/<int:id>', RunMethodView.as_view(), name='run_method'),
    path('<uuid:pk>', ExtractMetadataView.as_view(),name='extract_metadata'),
    path('clean/<uuid:pk>', CleanMetadataView.as_view(),name='clean_file_metadata'),
    # path('createviscol/<uuid:pk>/<int:id>',CreateVisColumnView.as_view(),name='create_vis_column'),
    path('findviscol/<uuid:pk>/<int:id>',FindColVisView.as_view(),name='find_column_visualization'),
    # path('createfiledist/<uuid:pk>',CreateFileDistView.as_view(),name='create_file_dist'),
    path('findfileres/<uuid:pk>',FindFileResultsView.as_view(),name='find_file_results'),
    # path('createnetwork/<uuid:pk>',CreateNetworkView.as_view(),name='create_network'),
]
