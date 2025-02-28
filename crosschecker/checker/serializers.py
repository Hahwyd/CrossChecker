from rest_framework import serializers
from .models import WikipediaArticle, WikipediaArticleJSON, Query, MyModel, CustomUser

class OpenAIGenerateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=2000)

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
        )

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = CustomUser.objects.filter(username=username).first()
        if user is None:
            raise serializers.ValidationError(
                'A user with that username was not found.'
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                'Incorrect credentials.'
            )
        

class WikipediaArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WikipediaArticle
        fields = '__all__'

class WikipediaArticleJSONSerializer(serializers.ModelSerializer):
    class Meta:
        model = WikipediaArticleJSON
        fields = '__all__'

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'