from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from base.models import *

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        # Render HTML template
        html_content = render_to_string('email_template.html', {'full_name': validated_data['username']})

        # Create plain text version of the HTML content for email clients that don't support HTML
        text_content = strip_tags(html_content)

        # Send email
        send_mail(
            subject='Welcome to our platform!',
            message=text_content,  # Use text content as the message
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_content,  # Attach HTML content as alternative content
            fail_silently=False,
        )

        return user

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

class EducationalOrganizationSerializer(ModelSerializer):
    class Meta:
        model = EducationalOrganizationModel
        fields = "__all__"

class SubdivisionSerializer(ModelSerializer):
    class Meta:
        model = SubdivisionModel
        fields = "__all__"

class ActivitySerializer(ModelSerializer):
    class Meta:
        model = ActivityModel
        fields = "__all__"

class PracticeSerializer(serializers.ModelSerializer):
    subdivision = serializers.PrimaryKeyRelatedField(queryset=SubdivisionModel.objects.all(), allow_null=True)
    activity = serializers.PrimaryKeyRelatedField(queryset=ActivityModel.objects.all(), many=True)
    class Meta:
        model = PracticeModel
        fields = "__all__"
