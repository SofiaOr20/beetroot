from rest_framework import serializers
from .models import Daybook


class DaybookSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        point = int(validated_data.pop('point'))
        return Daybook.objects.create(point=point, **validated_data)

    def update(self, instance, validated_data):
        instance.point += 1
        instance.save()

        return instance

    class Meta:
        model = Daybook
        fields = '__all__'

