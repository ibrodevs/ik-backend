from django.utils import timezone

from news.models import News, NewsCategory
from sights.models import Sight, SightImage
from departments.models import Department, DepartmentCategory, DepartmentLeader
from office_content.models import LeadershipMember, OfficialDocument, ProcurementItem, Project


def dashboard_context(request):
    """Provide dashboard statistics for the admin index page."""
    if not request.path.startswith('/admin/'):
        return {}

    now = timezone.now()
    thirty_days_ago = now - timezone.timedelta(days=30)

    # Counts
    news_total = News.objects.count()
    news_active = News.objects.filter(is_active=True).count()
    news_this_month = News.objects.filter(date__gte=thirty_days_ago).count()

    sights_total = Sight.objects.count()
    sights_active = Sight.objects.filter(is_active=True).count()
    sight_images_total = SightImage.objects.count()

    departments_total = Department.objects.count()
    departments_active = Department.objects.filter(is_active=True).count()
    dept_categories_total = DepartmentCategory.objects.count()
    leaders_total = DepartmentLeader.objects.count()

    documents_total = OfficialDocument.objects.count()
    documents_active = OfficialDocument.objects.filter(is_active=True).count()

    procurements_total = ProcurementItem.objects.count()
    procurements_active = ProcurementItem.objects.filter(is_active=True).count()

    projects_total = Project.objects.count()
    projects_active = Project.objects.filter(is_active=True).count()

    leadership_total = LeadershipMember.objects.count()

    # Recent news (last 5)
    recent_news = News.objects.select_related('category').order_by('-date')[:5]

    # Recent projects
    recent_projects = Project.objects.filter(is_active=True).order_by('-created_at')[:5]

    return {
        'dashboard': {
            'news_total': news_total,
            'news_active': news_active,
            'news_this_month': news_this_month,
            'sights_total': sights_total,
            'sights_active': sights_active,
            'sight_images_total': sight_images_total,
            'departments_total': departments_total,
            'departments_active': departments_active,
            'dept_categories_total': dept_categories_total,
            'leaders_total': leaders_total,
            'documents_total': documents_total,
            'documents_active': documents_active,
            'procurements_total': procurements_total,
            'procurements_active': procurements_active,
            'projects_total': projects_total,
            'projects_active': projects_active,
            'leadership_total': leadership_total,
            'recent_news': recent_news,
            'recent_projects': recent_projects,
        }
    }
