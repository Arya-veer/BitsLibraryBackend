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
        fields = ("description","is_set","data")
    
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
        return CommitteeMemberSerializer(obj.members.filter(is_present = True),many = True).data

class LibraryTeamMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = LibraryTeamMember
        exclude = ("team",)
    
class LibraryTeamSerializer(serializers.ModelSerializer):

    members = serializers.SerializerMethodField()

    class Meta:
        model = LibraryTeam
        fields = "__all__"
    
    def get_members(self,obj):
        return LibraryTeamMemberSerializer(obj.members.filter(is_present = True),many = True).data

class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = "__all__"