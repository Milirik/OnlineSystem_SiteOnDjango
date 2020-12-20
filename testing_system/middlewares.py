from django.db.models import Q
from .models import Course


def testing_system_context_processor(request):
    context = {}

    if request.user.is_active:
        context['user_courses'] = Course.objects.filter(Q(coursestudentaccess__student=request.user)
                                                        & Q(coursestudentaccess__access=True) & Q(is_shown=True))

    return context
