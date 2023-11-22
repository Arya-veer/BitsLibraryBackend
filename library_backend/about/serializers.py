from rest_framework import serializers

from .models import *


class LibraryOverviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryOverview
        fields = "__all__"

class LibraryCollectionDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryCollectionData
        # fields = "__all__"
        exclude = ("collection",)

class LibraryCollectionSerialzer(serializers.ModelSerializer):
    
    data = serializers.SerializerMethodField()

    class Meta:
        model = LibraryCollection
        fields = ("description","is_set","data","title")
    
    def get_data(self,obj):
        data_type = self.context['request'].query_params.get("type","int")
        if data_type == "int":
            return LibraryCollectionDataSerializer(LibraryCollectionData.objects.filter(collection=obj,is_int = True),many=True).data
        return LibraryCollectionDataSerializer(LibraryCollectionData.objects.filter(collection=obj,is_int = False),many=True).data

class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule
        exclude = ("parent",)

class TabularRuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = TabularRule
        exclude = ("parent",)

class LibraryRulesAndRegulationSerializer(serializers.ModelSerializer):

    rules = serializers.SerializerMethodField()
    tabular_rules = serializers.SerializerMethodField()

    class Meta:
        model = LibraryRulesAndRegulation
        fields = "__all__"
    
    def get_rules(self,obj):
        return RuleSerializer(obj.rules.all(),many=True).data

    def get_tabular_rules(self,obj):
        return TabularRuleSerializer(obj.tables.all(),many=True).data

class CommitteeMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryCommitteeMember
        exclude = ("committee",)
    
class LibraryCommitteeSerializer(serializers.ModelSerializer):

    members = serializers.SerializerMethodField()

    class Meta:
        model = LibraryCommittee
        fields = "__all__"
    
    def get_members(self,obj):
        return CommitteeMemberSerializer(obj.members.filter(is_present = True),many = True,context = self.context).data

class LibraryTeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryTeamMember
        exclude = ("team","id","is_present")
    
    
class LibraryTeamSerializer(serializers.ModelSerializer):

    members = serializers.SerializerMethodField()

    class Meta:
        model = LibraryTeam
        fields = "__all__"
    
    def get_members(self,obj):
        return LibraryTeamMemberSerializer(obj.members.filter(is_present = True),many = True,context = self.context).data


class LibraryBrochureSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryBrochure
        fields = "__all__"

class LibraryWebsiteUserGuideSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryWebsiteUserGuide
        fields = "__all__"

class LibraryCalendarsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryCalendar
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):

    url = serializers.SerializerMethodField()
    class Meta:
        model = Event
        # fields = "__all__"
        exclude = ("url_link","url_file")

    def get_url(self,obj):
        if obj.url_file:
            return self.context['request'].build_absolute_uri(obj.url_file.url)
        elif obj.url_link:
            return obj.url_link
        else:
            return None


class NewsSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    class Meta:
        model = News
        # fields = "__all__"
        exclude = ("url_link","url_file","source")

    def get_url(self,obj):
        if obj.url_file:
            return self.context['request'].build_absolute_uri(obj.url_file.url)
        elif obj.url_link:
            return obj.url_link
        else:
            return None

    def get_title(self,obj):
        if obj.source:
            return f"{obj.title} - {obj.source}"
        else:
            return obj.title
class BookMarqueeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookMarquee
        fields = ['isbn','id']

class LibraryTimingSerializer(serializers.ModelSerializer):

    opening_time = serializers.SerializerMethodField()
    closing_time = serializers.SerializerMethodField()
    is_currently_open = serializers.SerializerMethodField()
    holiday_reason = serializers.SerializerMethodField()
    class Meta:
        model = LibraryTiming
        fields = "__all__"
    
    def get_opening_time(self,obj):
        if self.context['timings']:
            return obj.opening_time.strftime("%I:%M %p")
        return "Not available for today"
    def get_closing_time(self,obj):
        if self.context['timings']:
            return obj.closing_time.strftime("%I:%M %p")
        return "Not available for today"

    def get_is_currently_open(self,obj):
        self.current_time = timezone.now().time()
        if self.context['timings'] == False:
            return None
        if obj.is_holiday:
            return False
        if self.current_time >= obj.opening_time and self.current_time <= obj.closing_time:
            return True
        else:
            return False
        
    def get_holiday_reason(self,obj):
        if self.get_is_currently_open(obj) is None:
            return "Data is not available for today! Please check library calendar"
        elif self.get_is_currently_open(obj):
            return "Library is open currently"
        elif obj.is_holiday:
            if obj.holiday_reason:
                return "Library is closed due to " + obj.holiday_reason
            else:
                return "Library is closed today"
        else:
            if self.current_time < obj.opening_time:
                return f"The library is temporarily shut down and is scheduled to resume services at {self.get_opening_time(obj)}"
            else:
                return f"Library is closed for the day"
    