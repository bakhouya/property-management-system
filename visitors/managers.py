from django.db import models
from django.utils import timezone
import hashlib
import uuid


class VisitorManager(models.Manager):

    # =========================================================================
    # Handle register visitor with visit in 24h
    # =========================================================================
    def record_visit(self, request, page_visited='/'):
        # =====================================================================
        # get data requrements from request 
        # =====================================================================
        ip_address = self.get_client_ip(request)
        browser_agent = request.META.get('HTTP_USER_AGENT', '')
        referrer = request.META.get('HTTP_REFERER', '')
        clean_referrer = self.clean_referrer(referrer)

        # =====================================================================
        # get or create visitor hash key if not exists in request
        # =====================================================================
        visitor_key = request.COOKIES.get('visitor_hash')
        if not visitor_key:
            visitor_key = self.create_visitor_hash(ip_address, browser_agent, clean_referrer)

        # =====================================================================
        # get or create new vistor if not exists in databse with some key
        # =====================================================================
        visitor, visitor_created = self.get_or_create(
            key=visitor_key,
            defaults={
                'ip_address': ip_address,
                'browser_agent': browser_agent,
                'country': self.get_country_from_ip(ip_address),
                'browser': self.get_browser_from_user_agent(browser_agent),
                'device_type': self.get_device_type(browser_agent)
            }
        )

        # =====================================================================
        # update data visitor 
        # =====================================================================
        visitor.last_visit = timezone.now()
        if not visitor.ip_address:
            visitor.ip_address = ip_address

        if not visitor.browser_agent:
            visitor.browser_agent = browser_agent

        if not visitor.country:
            visitor.country = self.get_country_from_ip(ip_address)

        if not visitor.browser:
            visitor.browser = self.get_browser_from_user_agent(browser_agent)


        # =====================================================================
        # check if this vistor has visit in 24h or not 
        # =====================================================================
        can_add_new_visit = self.is_new_visit(visitor)

        if can_add_new_visit:
            from .models import Visit
            Visit.objects.create(
                visitor=visitor,
                page_url=page_visited,
                page_title=request.GET.get('page_title', ''),
                referrer=clean_referrer
            )

        visitor.save()

        # =====================================================================
        #  Custom returb data
        # =====================================================================
        return {
            'visitor': visitor,
            'visitor_key': str(visitor.key),
            'is_new_visitor': visitor_created,
            'is_new_visit': can_add_new_visit
        }


    # =========================================================================
    # Create visitor hash key
    # =========================================================================
    def create_visitor_hash(self, ip_address, user_agent, referrer='direct'):
        data = f"{ip_address}-{user_agent}-{referrer}"
        return hashlib.sha256(data.encode()).hexdigest()
   
    # =========================================================================
    # Clean Referrer
    # =========================================================================
    def clean_referrer(self, ref):
        if not ref:
            return "direct"
        return ref.split('?')[0].strip()

    # =========================================================================
    # check if has visit for this visitor in 24h
    # =========================================================================
    def is_new_visit(self, visitor):
        from .models import Visit

        twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)

        has_recent_visit = Visit.objects.filter(
            visitor=visitor,
            visit_time__gte=twenty_four_hours_ago
        ).exists()

        return not has_recent_visit

    # =========================================================================
    # get ip address for this vistor
    # =========================================================================
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR', '0.0.0.0')

    # =========================================================================
    # get device type
    # =========================================================================
    def get_device_type(self, user_agent):
        if not user_agent:
            return 'Unknown'

        ua = user_agent.lower()
        if 'mobile' in ua:
            return 'Mobile'
        elif 'tablet' in ua:
            return 'Tablet'
        return 'Desktop'

    # =========================================================================
    # get country from ip
    # =========================================================================
    def get_country_from_ip(self, ip_address):
        try:
            import requests
            if ip_address and ip_address not in ['127.0.0.1', '0.0.0.0']:
                response = requests.get(f'http://ip-api.com/json/{ip_address}?fields=country',timeout=2)
                data = response.json()
                return data.get('country', 'Local')
        except:
            pass

        return 'Local'

    # =========================================================================
    # get browser agent 
    # =========================================================================
    def get_browser_from_user_agent(self, user_agent):
        if not user_agent:
            return 'null'

        ua = user_agent.lower()
        if 'chrome' in ua and 'edg' not in ua:
            return 'Chrome'
        elif 'firefox' in ua:
            return 'Firefox'
        elif 'safari' in ua and 'chrome' not in ua:
            return 'Safari'
        elif 'edg' in ua:
            return 'Edge'
        elif 'opera' in ua:
            return 'Opera'
        return 'null'
