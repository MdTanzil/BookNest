from datetime import datetime
from books.models import Category


def site_info(request):
    all_categories = Category.objects.all()[:10] or Category.objects.none()
    return {
        'site_name': 'BookNest',
        'site_tagline': 'Discover your next great read.',
        'current_year': datetime.now().year,
        'all_categories': all_categories,
    }
