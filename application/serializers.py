from rest_framework import serializers
from rest_framework.response import Response
from .models import Place, Adress, Category, Comment
from .utils import GetNote

    #Former API with Tastypie

        # fields = ('street_adress', 'postal_code', 'city', 'departement', 'region')
    # def get(self, request, *args, **kw):
    #     # Process any get params that you may need
    #     # If you don't need to process get params,
    #     # you can skip this part
    #     # get_arg1 = request.GET.get('arg1', None)
    #     # get_arg2 = request.GET.get('arg2', None)

    #     # Any URL parameters get passed in **kw
    #     # myClass = CalcClass(get_arg1, get_arg2, *args, **kw)
    #     # result = myClass.do_work()
    #     myNote = "ok vu"
    #     response = Response(result, status=status.HTTP_200_OK)
    #     return response
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['note'] = 'ok'
    #     return ret
    # def update(self, instance, validated_data):
    #     instance.myNote = "ok vu"
    #     return instance
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     # placeName = ret['name']
    #     # myPlace = Place.objects.get(name=placeName)
    #     # allComments = Comment.objects.all().filter(place_id=myPlace)
    #     ret['test'] = "is ok"
    #     # ret['note_can_you_enter'] = GetNote(allComments.filter(can_you_enter=True).count(), allComments.filter(can_you_enter =False).count())
    #     # ret['note_are_you_safe_enough'] = GetNote(allComments.filter(are_you_safe_enough=True).count(), allComments.filter(are_you_safe_enough =False).count())
    #     # ret['note_is_mixed_lockers'] = GetNote(allComments.filter(is_mixed_lockers=True).count(), allComments.filter(is_mixed_lockers =False).count())
    #     # ret['note_is_inclusive_lockers'] = GetNote(allComments.filter(is_inclusive_lockers=True).count(), allComments.filter(is_inclusive_lockers =False).count())
    #     # ret['note_has_respectful_staff'] = GetNote(allComments.filter(has_respectful_staff=True).count(), allComments.filter(has_respectful_staff =False).count())
    #     return ret

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('comment', 'date')

class AdressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adress
        fields = ('street_adress', 'postal_code', 'city', 'departement', 'region')


class PlaceSerializer(serializers.ModelSerializer):
    adress = AdressSerializer(many=False, read_only=True)
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Place
        fields = ('name', 'picture', 'description', 'website', 'contact_mail', 'contact_phone', 'comment', 'adress')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        placeName = ret['name']
        myPlace = Place.objects.get(name=placeName)
        allComments = Comment.objects.all().filter(place_id=myPlace)
        ret['global_note'] = GetNote(allComments.filter(score_global='P').count(), allComments.filter(score_global='N').count())
        ret['note_can_you_enter'] = GetNote(allComments.filter(can_you_enter=True).count(), allComments.filter(can_you_enter =False).count())
        ret['note_are_you_safe_enough'] = GetNote(allComments.filter(are_you_safe_enough=True).count(), allComments.filter(are_you_safe_enough =False).count())
        ret['note_is_mixed_lockers'] = GetNote(allComments.filter(is_mixed_lockers=True).count(), allComments.filter(is_mixed_lockers =False).count())
        ret['note_is_inclusive_lockers'] = GetNote(allComments.filter(is_inclusive_lockers=True).count(), allComments.filter(is_inclusive_lockers =False).count())
        ret['note_has_respectful_staff'] = GetNote(allComments.filter(has_respectful_staff=True).count(), allComments.filter(has_respectful_staff =False).count())
        return ret