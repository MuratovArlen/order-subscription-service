from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse
from subscriptions.models import UserSubscriptions
from datetime import date


class SubscriptionCheckMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        allowed_paths = [
            '/admin',
            '/api/tariffs',
            '/api/subscriptions'
        ]

        if any(request.path.startswith(p) for p in allowed_paths):
            return None


        if request.path.startswith('/api/orders'):
            if not request.user.is_authenticated:
                return JsonResponse({'detail': 'Вы не вошли в систему'}, status=401)

            has_active_sub = UserSubscriptions.objects.filter(
                user=request.user,
                end_date__gte=date.today()
            ).exists()

            if not has_active_sub:
                return JsonResponse({'detail': 'Нет активной подписки'}, status=403)

        return None
