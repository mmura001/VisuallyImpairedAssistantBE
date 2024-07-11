from rest_framework import serializers
from .models import WebsiteSnapshot

class WebsiteSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebsiteSnapshot
        fields = '__all__'


# serializers.py

# from rest_framework import serializers
# from .models import WebsiteSnapshot

# class WebsiteSnapshotSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WebsiteSnapshot
#         fields = ['website_url', 'date', 'snapshot_data']