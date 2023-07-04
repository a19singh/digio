from rest_framework import serializers


class DocumentSerializer(serializers.Serializer):
    """Serializer to validate input data."""

    name = serializers.CharField()
    identifier = serializers.CharField()
    reason = serializers.CharField()
    expire_in_days = serializers.IntegerField()
    display_on_page = serializers.CharField()
    notify_signers = serializers.BooleanField()
    file = serializers.FileField()


class DetailsSerializer(serializers.Serializer):
    """Serializer for document detail view."""

    doc_id = serializers.CharField()


class GetDocument(serializers.Serializer):
    """Serializer for document detail view."""

    doc_id = serializers.CharField()
