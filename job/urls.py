from django.urls import path
from . import views

urlpatterns = [
    path('jobpost/', views.JobPostViewSet.as_view(), name='jobPost'),
    path('jobpost/<int:pk>/', views.JobPostEditViewSet.as_view(), name='jobPostEdit'),
    path('jobproposal/', views.JobProposalViewset.as_view(), name='jobproposalview'),
    path('jobproposal/<int:pk>/', views.JobProposalEditView.as_view(), name='jobProposalEditview'),
    path('contract/', views.ContractView.as_view(), name='contract'),
]
