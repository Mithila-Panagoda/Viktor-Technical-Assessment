from .views import BookViewSet
from rest_framework_nested import routers

router = routers.SimpleRouter()
router.register('books', BookViewSet, 'book')

urlpatterns = router.urls