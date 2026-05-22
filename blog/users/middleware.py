from django.utils.timezone import now
from .models import UserSessionLog

class SessionTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Получаем или создаём сессию
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        # Получаем или создаём запись в логе сессий
        session_log, created = UserSessionLog.objects.get_or_create(
            session_key=session_key,
            defaults={
                'user': request.user if request.user.is_authenticated else None,
                'user_agent': request.META.get('HTTP_USER_AGENT', '')[:500],
                'ip_address': self.get_client_ip(request),
                'last_activity': now(),
                'page_views': 1
            }
        )
        
        # Если сессия уже существует, обновляем данные
        if not created:
            session_log.last_activity = now()
            session_log.page_views += 1
            if request.user.is_authenticated and not session_log.user:
                session_log.user = request.user
            session_log.save()
        
        # Сохраняем session_log в request для использования в других местах
        request.session_log = session_log
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip




