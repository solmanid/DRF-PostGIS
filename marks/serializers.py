# DRF
from rest_framework import serializers

# Django local
from .models import PlacePoints


class MarksListSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    map_location = serializers.SerializerMethodField()

    class Meta:
        model = PlacePoints
        fields = [
            'user',
            'description',
            'picture',
            'likes',
            'map_location',
            'created',
            'status',
        ]

    def get_map_location(self, obj: PlacePoints):
        lat = obj.location[0]
        lng = obj.location[1]

        return F"{lng},{lat}"


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
