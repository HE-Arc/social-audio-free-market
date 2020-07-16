from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from .models import Tag, Sample, UserProfile, UserSampleDownload, SampleLike

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    password_current = serializers.CharField(write_only=True, required=False)
    password_min_length = 8
    
    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')
        password_current = data.get('password_current')

        # User create or user password patch
        if not self.partial or (self.partial and password):
            if self.partial and not check_password(password_current, self.instance.password):
                raise serializers.ValidationError('Invalid current password.')

            if self.partial and check_password(password, self.instance.password):
                raise serializers.ValidationError('The new password must be different than the current one.')

            if len(password) < self.password_min_length:
                raise serializers.ValidationError('Password length must be at least {0} characters.'.format(self.password_min_length))

            if password != password_confirm:
                raise serializers.ValidationError('Password confirmation does not match.')

        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        # Creates a UserProfile when a new User is created
        UserProfile.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        if validated_data.get('username'):
            instance.username = validated_data.get('username')

        if validated_data.get('email'):
            instance.email = validated_data.get('email')

        if validated_data.get('password'):
            instance.set_password(validated_data.get('password'))
        
        instance.save()

        return instance

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'password_confirm', 'password_current', 'date_joined']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField()
        
    def validate(self, data):
        username = ''
        if 'username' in data:
            username = data['username']
        elif 'email' in data:
            try:
                username = User.objects.get(email=data['email']).username
            except User.DoesNotExist:
                username = ''

        user = authenticate(username=username, password=data['password'])

        if user:
            return user

        raise serializers.ValidationError('Wrong credentials')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class SampleForkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Sample
        fields = '__all__'


class SampleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, required=False)
    forks = SampleForkSerializer(write_only=True, many=True, required=False)

    def create(self, validated_data):
        sample = Sample.objects.create(**validated_data)

        sample.deduce_properties()
        sample.save()

        return sample

    class Meta:
        model = Sample
        fields = '__all__'


class UserDownloadSerializer(serializers.ModelSerializer):
    sample = SampleSerializer()

    class Meta:
        model = UserSampleDownload
        fields = '__all__'
        

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = '__all__'


class SampleLikeSerializer(serializers.ModelSerializer):
    sample = SampleSerializer()

    class Meta:
        model = SampleLike
        fields = ['sample', 'datetime_like']
