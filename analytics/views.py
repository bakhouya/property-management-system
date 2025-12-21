from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.contrib.auth import get_user_model
from visitors.models import Visit, Visitor
from properties.models import Property
User = get_user_model()


# ====================================================================
# Get Statistic Visistis use resource
# ====================================================================
class DetailedSourceAnalysisView(APIView):
    def get(self, request):
        try:
            visits = Visit.objects.exclude(referrer__isnull=True).exclude(referrer='')            
            if not visits.exists():
                return Response({'detailed_analysis': {}, 'message': "No Data Fount" })

            sources_analysis = self.analyze_main_sources(visits)
            detailed_analysis = {}          
            for source in sources_analysis:
                source_name = source['source']
                source_visits = visits.filter(
                    referrer__icontains=self.get_source_domain(source_name)
                ) if source_name != 'direct' else visits.filter(referrer__isnull=True) | visits.filter(referrer='')
                detailed_analysis[source_name] = {
                    'total': source['total_visits'],
                    'percentage': source['percentage'],
                    'breakdown': source['details']
                }
                top_refs = self.get_top_referrers(source_visits, 3)
                if top_refs:
                    detailed_analysis[source_name]['top_referrers'] = top_refs
            
            return Response({'detailed_analysis': detailed_analysis}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def analyze_main_sources(self, visits):
        sources = {}
        
        for visit in visits:
            referrer = visit.referrer
            main_source = self.get_main_source(referrer)
            
            if main_source not in sources:
                sources[main_source] = {'total_visits': 0, 'referrers': {}}
            
            sources[main_source]['total_visits'] += 1
            
            sub_source = self.get_sub_source(referrer, main_source)
            if sub_source not in sources[main_source]['referrers']:
                sources[main_source]['referrers'][sub_source] = 0
            sources[main_source]['referrers'][sub_source] += 1
        
        result = []
        for source_name, data in sources.items():
            total = data['total_visits']
            percentage = (total / visits.count()) * 100 if visits.count() > 0 else 0
            details = self.analyze_source_referrers(data['referrers'])            
            result.append({
                'source': source_name,
                'total_visits': total,
                'percentage': round(percentage, 2),
                'details': details
            })
        result.sort(key=lambda x: x['total_visits'], reverse=True)
        return result
    
    def get_main_source(self, referrer):
        if not referrer or 'direct' in referrer.lower():
            return 'direct'
        
        referrer_lower = referrer.lower()
        sources_map = {
            'facebook.com': 'facebook',
            'fb.com': 'facebook',
            'instagram.com': 'instagram',
            'twitter.com': 'twitter',
            'x.com': 'twitter',
            'linkedin.com': 'linkedin',
            'tiktok.com': 'tiktok',
            'youtube.com': 'youtube',
            'google.com': 'google',
            'bing.com': 'bing',
            'yahoo.com': 'yahoo',
        }
        
        for domain, source in sources_map.items():
            if domain in referrer_lower:
                return source
        
        return 'other'
    
    def get_sub_source(self, referrer, main_source):
        referrer_lower = referrer.lower()
        
        if main_source == 'facebook':
            if '/ads/' in referrer_lower or 'utm_campaign=' in referrer_lower:
                return 'ads'
            elif '/groups/' in referrer_lower:
                return 'groups'
            elif '/pages/' in referrer_lower:
                return 'pages'
            elif '/events/' in referrer_lower:
                return 'events'
            elif '/marketplace/' in referrer_lower:
                return 'marketplace'
            else:
                return 'posts'
        
        elif main_source == 'google':
            if '/search' in referrer_lower:
                return 'search'
            elif '/ads/' in referrer_lower:
                return 'ads'
            elif '/maps/' in referrer_lower:
                return 'maps'
            else:
                return 'other'
        
        elif main_source == 'instagram':
            if '/p/' in referrer_lower:
                return 'posts'
            elif '/reel/' in referrer_lower:
                return 'reels'
            elif '/stories/' in referrer_lower:
                return 'stories'
            else:
                return 'other'
        
        elif main_source == 'tiktok':
            if '/video/' in referrer_lower:
                return 'videos'
            elif '/ads/' in referrer_lower:
                return 'ads'
            else:
                return 'other'
        
        return 'general'
    
    def analyze_source_referrers(self, referrers_dict):
        total = sum(referrers_dict.values())
        
        details = {}
        for sub_source, count in referrers_dict.items():
            percentage = (count / total) * 100 if total > 0 else 0
            details[sub_source] = {'visits': count, 'percentage': round(percentage, 2)}
        
        return details
    
    def get_source_domain(self, source_name):
        domains = {
            'facebook': 'facebook.com',
            'google': 'google.com',
            'instagram': 'instagram.com',
            'tiktok': 'tiktok.com',
            'twitter': 'twitter.com',
            'linkedin': 'linkedin.com',
            'youtube': 'youtube.com',
            'bing': 'bing.com',
            'yahoo': 'yahoo.com',
        }
        return domains.get(source_name, source_name)
    
    def get_top_referrers(self, visits, limit=3):
        from django.db.models import Count
        
        top = visits.values('referrer').annotate(count=Count('id')).order_by('-count')[:limit]
        
        return [
            {
                'url': item['referrer'][:80],
                'visits': item['count']
            }
            for item in top
        ]
# ====================================================================
# 
# 
# ====================================================================
# get statistic users and visitors and properties
# ====================================================================
class SimpleDashboardStatsAPIView(APIView):
    def get(self, request):
        try:
            today = timezone.now().date()
            users_count = User.objects.filter(is_superuser=False, is_staff=False).count()
            today_users_count = User.objects.filter(is_superuser=False, is_staff=False, date_joined__date=today).count()
            visitors_count = Visitor.objects.count()
            today_visits_count = Visitor.objects.filter(first_visit__date=today).count()
            properties_count = Property.objects.count()
            today_properties_count = Property.objects.filter(created_at__date=today).count()
            data = {
                'users_count': users_count,
                'today_registered_users': today_users_count,
                'all_visitors': visitors_count,
                'today_visitors': today_visits_count,
                'all_properties': properties_count,
                'today_properties': today_properties_count,
                'date': today.isoformat(),
                'timestamp': timezone.now().isoformat()
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# ====================================================================
# 
# 
# ====================================================================
# statistic visitis
# ====================================================================
class VisitStatsAPIView(APIView):
    def get(self, request):
        try:
            today = timezone.now().date()
            all_visits_count = Visit.objects.count()
            visitors_count = Visitor.objects.count()
            today_visits_count = Visit.objects.filter(visit_time__date=today).count()
            if all_visits_count > 0:
                today_percentage = (today_visits_count / visitors_count) * 100
            else:
                today_percentage = 0

            data = {
                'total_visitors': visitors_count,
                'total_visits': all_visits_count,
                'today_visits': today_visits_count,
                'today_percentage': round(today_percentage, 2),
                'date': today.isoformat(),
            }
            
            return Response(data, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# ====================================================================












