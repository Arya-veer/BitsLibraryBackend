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
        return LibraryCollectionDataSerializer(LibraryCollectionData.objects.filter(collection=obj),many=True).data

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

class LibraryTimingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryTiming
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
        return f"{obj.title} - {obj.source}"

class BookMarqueeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookMarquee
        fields = ['isbn','id']
