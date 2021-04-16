from django.utils import timezone
from django.db import transaction

from rest_framework import serializers
from .models import *


class ChoiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField()


class QuestionSerializer(serializers.ModelSerializer):
    """
    Question serializer
    make choices emty if question_type is text
    """
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'question_type', 'survey', 'choices')
        read_only_fields = ('id',)

    def validate(self, data):
        # The keys can be missing in partial updates
        if "question_type" in data and "choices" in data:
            if data["question_type"] != Question.TEXT and data["choices"] == []:
                raise serializers.ValidationError({
                    "choices": "Choices cannot be empty",
                })

        # if "choices" not in data and data["question_type"] != Question.TEXT:
        #     raise serializers.ValidationError({
        #         "choices": "Choices cannot be empty",
        #     })

        return super(QuestionSerializer, self).validate(data)

    def create(self, validated_data):
        try:
            choices = validated_data.pop('choices', [])
            with transaction.atomic():
                instance = Question.objects.create(**validated_data)
                # bulk_create if question_type not text
                if instance.question_type != Question.TEXT:
                    Choice.objects.bulk_create([
                        Choice(question=instance, **choice) for choice in choices
                    ])
            return instance
        except Exception as ex:
            raise serializers.ValidationError(ex)

    def update(self, instance, validated_data):
        try:
            choices = validated_data.pop('choices', [])
            instance = super().update(instance, validated_data)
            # remove and bulk_create if question_type not text
            if choices:
                Choice.objects.filter(question=instance).delete()
            if instance.question_type != Question.TEXT:
                Choice.objects.bulk_create([
                    Choice(question=instance, **choice) for choice in choices
                ])
            return instance
        except Exception as ex:
            raise serializers.ValidationError(ex)


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ('id', 'name', 'description', 'start_date', 'end_date',)
        read_only_fields = ('id',)

    def validate(self, data):
        # The keys can be missing in partial updates
        if "start_date" in data and "end_date" in data:
            if data["start_date"] > data["end_date"]:
                raise serializers.ValidationError({
                    "start_date": "Start date cannot be greater than end date",
                })

        if "end_date" in data and data["end_date"] < timezone.now():
            raise serializers.ValidationError({
                "end_date": "End date must be greater than now",
            })

        return super(SurveySerializer, self).validate(data)


class SurveyDetailSerializer(SurveySerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta(SurveySerializer.Meta):
        fields = SurveySerializer.Meta.fields + ('questions',)


class SurveyUpdateSerializer(SurveySerializer):

    class Meta(SurveySerializer.Meta):
        read_only_fields = ('start_date',)
