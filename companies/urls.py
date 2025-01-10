from django.urls import path
from companies.views.companies import (
    CompanyAdminListView,
    CompanyAdminDetailView,
    CompanyOwnerDetailView,
    GetCompanyDetails,
    ChatListView,
    CreateChatView,
    RejectScheduleMeetingView,
    ChatMessagesView
)

urlpatterns = [
    # Rutas para administradores
    path('admin/companies/', CompanyAdminListView.as_view(), name='admin-company-list'),
    path('admin/companies/<int:pk>/', CompanyAdminDetailView.as_view(), name='admin-company-detail'),
    path('details/<int:company_id>/', GetCompanyDetails.as_view(), name='admin-company-detail'),
    
    # Rutas para dueños de empresas
    path('owner/company/', CompanyOwnerDetailView.as_view(), name='owner-company-detail'),
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path("create-chat/", CreateChatView.as_view(), name="create_chat"),
    path("reject-meeting/", RejectScheduleMeetingView.as_view(), name="reject-meeting"),
    path("chats/<int:chat_id>/messages/", ChatMessagesView.as_view(), name="chat-messages"),

]
