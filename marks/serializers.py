from rest_framework import serializers

from .models import PlacePoints


class MarksListSerializers(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = PlacePoints
        fields = '__all__'


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
