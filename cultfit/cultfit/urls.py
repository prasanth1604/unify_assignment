from django.contrib import admin
from django.urls import path
from core.views import AllClassesView, ClassesByClientView, BookClassView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('classes/', AllClassesView.as_view(), name='all_classes'),
    path('book/', BookClassView.as_view(), name='book_class'),
    path('bookings/<str:email_id>/', ClassesByClientView.as_view(), name='classes_by_client'),
]
