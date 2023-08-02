# DRF
from rest_framework import serializers

# Django local
from .models import PlacePoints


class MarksListSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    map_location = serializers.SerializerMethodField()
    failed = serializers.IntegerField(default=0)

    class Meta:
        model = PlacePoints
        fields = [
            'user',
            'description',
            'picture',
            'likes',
            'map_location',
            'failed',
            'status',
            'is_accepted',
            'created',
        ]

    def get_map_location(self, obj: PlacePoints):
        lat = obj.location[0]
        lng = obj.location[1]

        return F"{lng},{lat}"

    def to_representation(self, instance: PlacePoints):
        representation = super().to_representation(instance)
        representation['failed'] = instance.count_of_failed

        return representation


class MarksAddSerializers(serializers.ModelSerializer):
    lat = serializers.CharField(max_length=300)
    lng = serializers.CharField(max_length=300)

    class Meta:
        model = PlacePoints
        fields = [
            'description',
            'lat',
            'lng',
        ]


class UpdateMarkSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    lat = serializers.CharField(max_length=300, required=False)
    lng = serializers.CharField(max_length=300, required=False)

    class Meta:
        model = PlacePoints
        fields = [
            'user',
            'likes',
            'description',
            'picture',
            'lat',
            'lng',
        ]
        # exclude = [
        #     'is_accepted',
        #     'status',
        # ]
