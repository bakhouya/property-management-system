
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.db.models import Count, Avg, Q, Sum
from django.utils import timezone
from datetime import timedelta
from accounts.models import User
from properties.models import Property
from visitors.models import Visitor, Visit 
from chats.models import Conversation, Message
from categories.models import MainCategory, SubCategory



class DailySimpleStatsView(APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        try:
            today = timezone.now().date()
            
    
            visitors_today = Visitor.objects.filter(first_visit__date=today).count()
            total_visitors = Visitor.objects.count()
            

            new_users_today = User.objects.filter(date_joined__date=today, is_staff=False).count()        
            total_regular_users = User.objects.filter(is_staff=False).count()
            
            visits_today = Visit.objects.filter(visit_date=today).count()
            total_visits = Visit.objects.count()

            if visitors_today > 0:
                daily_conversion_rate = (new_users_today / visitors_today) * 100
            else:
                daily_conversion_rate = 0
            
            if total_visitors > 0:
                total_conversion_rate = (total_regular_users / total_visitors) * 100
            else:
                total_conversion_rate = 0
            
            conversion_rate_difference = daily_conversion_rate - total_conversion_rate
            
            data = {
                'date': today.isoformat(),
                
                'visitors': {
                    'today': visitors_today,
                    'total': total_visitors
                },

                'visits': {
                    'today': visits_today,
                    'total': total_visits
                },
                
                'users': {
                    'today': new_users_today,
                    'total': total_regular_users
                },
                
                'conversion_rates': {
                    'daily': round(daily_conversion_rate, 2),
                    'total': round(total_conversion_rate, 2),
                    'difference': round(conversion_rate_difference, 2)
                }
            }
            
            return Response(data, status=status.HTTP_200_OK)



        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DetailedSourceAnalysisView(APIView):
    """تحليل مفصل لمصادر الزيارات"""
    
    def get(self, request):
        try:
            # استبعاد الزيارات بدون referrer
            visits = Visit.objects.exclude(referrer__isnull=True).exclude(referrer='')
            
            if not visits.exists():
                return Response({
                    'detailed_analysis': {},
                    'message': 'لا توجد بيانات referrer في قاعدة البيانات'
                })
            
            # تحليل المصادر الرئيسية
            sources_analysis = self.analyze_main_sources(visits)
            
            # إنشاء detailed_analysis فقط
            detailed_analysis = {}
            
            for source in sources_analysis:
                source_name = source['source']
                
                # تجميع زيارات هذا المصدر
                source_visits = visits.filter(
                    referrer__icontains=self.get_source_domain(source_name)
                ) if source_name != 'direct' else visits.filter(referrer__isnull=True) | visits.filter(referrer='')
                
                # إضافة البيانات الأساسية
                detailed_analysis[source_name] = {
                    'total': source['total_visits'],
                    'percentage': source['percentage'],
                    'breakdown': source['details']
                }
                
                # إضافة top_referrers فقط إذا كانت موجودة
                top_refs = self.get_top_referrers(source_visits, 3)
                if top_refs:
                    detailed_analysis[source_name]['top_referrers'] = top_refs
            
            # إرجاع detailed_analysis فقط
            return Response({
                'detailed_analysis': detailed_analysis
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def analyze_main_sources(self, visits):
        """تحليل المصادر الرئيسية"""
        sources = {}
        
        for visit in visits:
            referrer = visit.referrer
            main_source = self.get_main_source(referrer)
            
            if main_source not in sources:
                sources[main_source] = {
                    'total_visits': 0,
                    'referrers': {}
                }
            
            sources[main_source]['total_visits'] += 1
            
            sub_source = self.get_sub_source(referrer, main_source)
            if sub_source not in sources[main_source]['referrers']:
                sources[main_source]['referrers'][sub_source] = 0
            sources[main_source]['referrers'][sub_source] += 1
        
        # تحويل إلى قائمة
        result = []
        for source_name, data in sources.items():
            total = data['total_visits']
            percentage = (total / visits.count()) * 100 if visits.count() > 0 else 0
            
            # تحليل التفاصيل
            details = self.analyze_source_referrers(data['referrers'])
            
            result.append({
                'source': source_name,
                'total_visits': total,
                'percentage': round(percentage, 2),
                'details': details
            })
        
        # ترتيب تنازلي
        result.sort(key=lambda x: x['total_visits'], reverse=True)
        return result
    
    def get_main_source(self, referrer):
        """الحصول على المصدر الرئيسي"""
        if not referrer or 'direct' in referrer.lower():
            return 'direct'
        
        referrer_lower = referrer.lower()
        
        # قائمة المصادر الرئيسية
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
        """الحصول على المصدر الفرعي"""
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
        """تحليل الروابط داخل المصدر"""
        total = sum(referrers_dict.values())
        
        details = {}
        for sub_source, count in referrers_dict.items():
            percentage = (count / total) * 100 if total > 0 else 0
            details[sub_source] = {
                'visits': count,
                'percentage': round(percentage, 2)
            }
        
        return details
    
    def get_source_domain(self, source_name):
        """الحصول على النطاق"""
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
        """أكثر الروابط زيارة"""
        from django.db.models import Count
        
        top = visits.values('referrer').annotate(
            count=Count('id')
        ).order_by('-count')[:limit]
        
        return [
            {
                'url': item['referrer'][:80],
                'visits': item['count']
            }
            for item in top
        ]











# ============ إعداد عام للصلاحيات ============
class AnalyticsPermission(permissions.BasePermission):
    """
    صلاحية مخصصة للتحقق من أن المستخدم مسؤول أو لديه صلاحية الوصول للإحصائيات.
    (يمكنك تعديله بناءً على نظام الصلاحيات الخاص بك)
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

# ============ 1. ملخص النظام العام ============
class SystemSummaryView(APIView):
    # permission_classes = [AnalyticsPermission]
    def get(self, request):
        try:
            total_users = User.objects.count()
            active_properties = Property.objects.filter(status=True).count()
            last_24h = timezone.now() - timedelta(hours=24)
            visitors_today = Visitor.objects.filter(first_visit__gte=last_24h).count()

            data = {
                'summary': {
                    'total_users': total_users,
                    'active_users': User.objects.filter(is_active=True).count(),
                    'total_properties': Property.objects.count(),
                    'active_properties': active_properties,
                    'total_conversations': Conversation.objects.count(),
                    'visitors_today': visitors_today,
                    'total_visitors': Visitor.objects.count(),
                },
                'timestamp': timezone.now().isoformat()
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': {str(e)}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ============ 2. إحصائيات العقارات ============
class PropertyStatsView(APIView):
    # permission_classes = [AnalyticsPermission]

    def get(self, request):
        try:
            # الإحصائيات حسب التصنيف الرئيسي
            by_main_category = MainCategory.objects.annotate(property_count=Count('properties')).values('title', 'property_count')

            # الإحصائيات حسب الحالة
            by_status = Property.objects.values('status').annotate(count=Count('id')).order_by('status')

            # إحصائيات التفاعل
            total_likes = Property.objects.aggregate(total=Sum('likes_count'))['total'] or 0

            data = {
                'property_stats': {
                    'by_main_category': list(by_main_category),
                    'by_status': list(by_status),
                    'average_price': Property.objects.filter(
                        price__isnull=False
                    ).aggregate(avg=Avg('price'))['avg'],
                    'total_likes': total_likes,
                    'total_favorites': Property.objects.aggregate(
                        total=Sum('favorites_count')
                    )['total'] or 0,
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'خطأ في جلب إحصائيات العقارات: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ============ 3. إحصائيات المستخدمين ============
class UserStatsView(APIView):
    permission_classes = [AnalyticsPermission]

    def get(self, request):
        try:
            today = timezone.now().date()
            week_ago = today - timedelta(days=7)

            data = {
                'user_stats': {
                    'total_users': User.objects.count(),
                    'new_users_today': User.objects.filter(
                        date_joined__date=today
                    ).count(),
                    'new_users_this_week': User.objects.filter(
                        date_joined__date__gte=week_ago
                    ).count(),
                    'active_users_last_7_days': User.objects.filter(
                        last_login__date__gte=week_ago
                    ).count(),
                    'users_by_role': {
                        'admin': User.objects.filter(is_staff=True).count(),
                        'active': User.objects.filter(is_active=True).count(),
                        'inactive': User.objects.filter(is_active=False).count(),
                    }
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'خطأ في جلب إحصائيات المستخدمين: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ============ 4. إحصائيات الزوار ============
class VisitorStatsView(APIView):
    permission_classes = [AnalyticsPermission]

    def get(self, request):
        try:
            today = timezone.now().date()

            data = {
                'visitor_stats': {
                    'total_visitors': Visitor.objects.count(),
                    'visitors_today': Visitor.objects.filter(
                        created_at__date=today
                    ).count(),
                    'unique_visitors': Visitor.objects.values('ip_address').distinct().count(),
                    # ملاحظة: قد تحتاج حقول إضافية في نموذج Visitor لتتبع المصدر
                    'visitors_by_source': {
                        'direct': Visitor.objects.filter(source='direct').count(),
                        'google': Visitor.objects.filter(source='google').count(),
                        'facebook': Visitor.objects.filter(source='facebook').count(),
                    }
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'خطأ في جلب إحصائيات الزوار: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ============ 5. إحصائيات المحادثات ============
class ConversationStatsView(APIView):
    permission_classes = [AnalyticsPermission]

    def get(self, request):
        try:
            today = timezone.now().date()
            today_start = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))

            data = {
                'conversation_stats': {
                    'total_conversations': Conversation.objects.count(),
                    'active_conversations': Conversation.objects.filter(
                        date_last_message__date=today
                    ).count(),
                    'messages_today': Message.objects.filter(
                        created_at__date=today
                    ).count(),
                    'total_messages': Message.objects.count(),
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'خطأ في جلب إحصائيات المحادثات: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# ============ 6. إحصائيات حسب الفترة ============
class PeriodStatsView(APIView):
    permission_classes = [AnalyticsPermission]

    def get(self, request, period):
        """
        period: يمكن أن تكون 'today', 'week', 'month', 'year'
        """
        try:
            now = timezone.now()
            period_map = {
                'today': now - timedelta(hours=24),
                'week': now - timedelta(days=7),
                'month': now - timedelta(days=30),
                'year': now - timedelta(days=365),
            }

            if period not in period_map:
                return Response(
                    {'error': 'الفترة يجب أن تكون: today, week, month, أو year'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            start_date = period_map[period]

            data = {
                'period': period,
                'start_date': start_date.isoformat(),
                'end_date': now.isoformat(),
                'stats': {
                    'new_users': User.objects.filter(
                        date_joined__gte=start_date
                    ).count(),
                    'new_properties': Property.objects.filter(
                        created_at__gte=start_date
                    ).count(),
                    'new_visitors': Visitor.objects.filter(
                        created_at__gte=start_date
                    ).count(),
                    'new_messages': Message.objects.filter(
                        created_at__gte=start_date
                    ).count(),
                    'new_conversations': Conversation.objects.filter(
                        created_at__gte=start_date
                    ).count(),
                }
            }
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'خطأ في جلب إحصائيات الفترة: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
