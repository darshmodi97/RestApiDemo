from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import serializers
from django.contrib.auth.models import User, update_last_login
from rest_framework_jwt.settings import api_settings

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER


class UserSerializer(serializers.HyperlinkedModelSerializer):
    detail_url = serializers.HyperlinkedIdentityField(view_name='account:show_profile', read_only=True,
                                                      lookup_field='pk')

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'detail_url',)
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'placeholder': 'Password'}}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserUpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff')

    def update(self, instance, validated_data):

        instance.username = validated_data.get('username') \
            if not validated_data.get('email') is '' else instance.username

        instance.email = validated_data.get('email') if not validated_data.get('email') is '' else instance.email

        instance.first_name = validated_data.get('first_name') \
            if not validated_data.get('first_name') is '' else instance.first_name

        instance.last_name = validated_data.get('last_name') \
            if not validated_data.get('last_name') is '' else instance.last_name

        instance.is_superuser = validated_data.get('is_superuser')
        instance.is_staff = validated_data.get('is_staff')
        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        instance.save()
        return instance


class UserDetailSerializer(serializers.HyperlinkedModelSerializer):
    change_password = serializers.HyperlinkedIdentityField(view_name='account:change_password', read_only=True,
                                                           lookup_field='pk')

    class Meta:
        model = User
        fields = (
            'username', 'password', 'first_name', 'last_name', 'email', 'is_superuser', 'is_staff', 'change_password')


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        try:
            username = User.objects.get(email=email).username

        except ObjectDoesNotExist:
            raise Http404
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )
        return {
            'email': user.email,
            'token': jwt_token
        }


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(max_length=150, write_only=True)
    new_password = serializers.CharField(max_length=150, write_only=True)
    new_password2 = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_password2')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_old_password(self, value):
        instance = self._kwargs['instance']  # model object
        print("---", instance)
        user = self.context['request'].user
        if user.id != instance.id:
            raise serializers.ValidationError("You don't have permission for this user.")
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(" Please enter correct old password.")

        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.id != instance.id:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.set_password(validated_data['new_password2'])
        instance.save()
        return instance