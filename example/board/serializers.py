from rest_framework import serializers as sz

from .models import Major, Post, User, Category

class CategorySerializer(sz.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'code')


class MajorSerializer(sz.ModelSerializer):
    class Meta:
        model = Major
        fields = ('name',)


class UserSerializer(sz.ModelSerializer):
    majors = MajorSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('account', 'majors')


class PostSerializer(sz.ModelSerializer):
    likes_count = sz.SerializerMethodField(method_name='get_likes_count')
    is_liked = sz.SerializerMethodField(method_name='get_is_liked')

    class Meta:
        model = Post
        fields = ('title', 'content', 'category', 'author', 'likes_count', 'is_liked')

    # ForeignKey 필드인 category, author를 serialize하기 위해 to_representation을 override합니다.
    # 참고 : https://gaussian37.github.io/python-rest-nested-serializer/
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['category'] = CategorySerializer(instance.category).data
        response['author'] = UserSerializer(instance.author).data
        
        return response

    def get_likes_count(self, obj):
        liked_users = obj.like_users.all()
        likes_count = liked_users.count()

        return likes_count
    
    def get_is_liked(self, obj):
        user = self.context['request'].user

        if user and user in obj.like_users.all():
            return True
        else:
            return False

