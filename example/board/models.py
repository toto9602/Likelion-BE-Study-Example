from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# User 모델 작성 부분
# UserManager 작성과 AbstractBaseUser 상속 부분은 참고만 해주세요 :) 

class Major(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

# User를 생성할 때 사용하는 헬퍼 클래스인 BaseUserManager를 상속합니다.
# User를 생성할 때의 행위를 지정합니다. 
class UserManager(BaseUserManager):
    def create_user(self, account, password):
        # User 생성시 아이디와 비밀번호가 없다면 에러를 호출합니다.
        if not account:
            raise ValueError("must have an account")
        if not password:
            raise ValueError("must have a password")
        
        # 이 Manager가 가리키는 모델 
        # 아래 URL 참고
        # https://iamthejiheee.tistory.com/78
        # https://stackoverflow.com/questions/51163088/self-model-in-django-custom-usermanager
        user = self.model(
            account=account
        )
        # 비밀번호 세팅(hash)
        user.set_password(password)

        user.save(using=self.db)

        return user

    def create_superuser(self, account, password):

        user = self.create_user(
            account=account,
            password=password
        )

        # superuser 생성이기 때문에 is_admin 속성과 is_superuser 속성을 True로 하여 저장합니다.
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
            
        user.save(using=self.db)
        return user


# AbstractBaseUser와 PermissionsMixin을 상속한 User 모델을 작성합니다.
# PermissionsMixin은 계정 관리 권한을 제어하는 메서드를 제공한다고 하네요.
# 참고 : https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#custom-users-and-permissions
class User(AbstractBaseUser, PermissionsMixin):
    account = models.CharField(max_length=50, unique=True) # USERNAME_FIELD는 unique해야 합니다.
    password = models.CharField(max_length=200)
    majors = models.ManyToManyField(Major)

    is_staff = models.BooleanField(
        default=False
    )
    objects = UserManager()
    USERNAME_FIELD = 'account'

    def __str__(self):
        return self.account


# 게시글 카테고리
# 요구사항 3. "카테고리 이름" 혹은 "카테고리 코드"로 게시글 조회 가능
class Category(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=20)

    def __str__(self):
        return self.name + self.code

# 게시글
# 제목과 내용을 갖습니다.
# 하나의 게시글은 하나의 카테고리와, 하나의 카테고리는 여러 게시글과 관계를 갖습니다 (일대다)
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    # related_name 작성을 통해 관계간 충돌을 방지합니다.
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    like_users = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        return self.title


# 게시글의 댓글
# 내용을 갖습니다
# 하나의 게시글은 여러 개의 댓글을 갖습니다. (일대다)
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()

    def __str__(self):
        return self.content


