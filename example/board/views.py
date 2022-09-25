from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer
from .models import Post, Category, User

# APIView를 상속받아 CBV로 작성합니다.
# APIView를 상속받은 클래스 안에 request method에 맞는 함수들을 정의해주면
# 각각의 요청은 request method 이름에 맞게 구분되어 그에 맞는 결과를 반환합니다.
class PostListAPIView(APIView):
    serializer_class = PostSerializer
    # serializer에 context라는 key로 추가적인 데이터를 포함합니다.
    # 해당 예시에서는 추가 데이터가 request 자체로, request.user를 활용하기 위해 필요합니다.
    def get_seri(self, *args, **kwargs):
        serializer = PostSerializer
        kwargs['context'] = {'request':self.request}

        return serializer(*args, **kwargs)

    # URL : board/posts
    # HTTP Method : GET
    def get(self, request):
        # 기본적인, 모든 Post를 반환하는 endpoint입니다.
        # 요구사항대로, category로 필터링하는 endpoint는 직접 작성해 보시길 바랍니다!
        # Post.objects.filter(~~~)
        posts = Post.objects.all()
        serializer = self.get_seri(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # URL : board/posts
    # HTTP Method : GET
    def post(self, request):
        # Post를 생성하는 endpoint입니다.
        # title, content, 그리고 category_code를 JSON 형태로 입력받는 것을 전제하였습니다.
        # 사용자가 로그인된 상태임을 가정하였습니다.
        # 저는 Django의 기본 로그인으로 테스트하였지만, 3주차 과제에 맞게 인증/인가를 반영해 보시길 바랍니다!
        
        # 데이터 dict 타입에 title, content, author, category 값을 넣어 줍니다.
        data = {}

        data['title'] = request.data['title']
        data['content'] = request.data['content']
        data['author'] = User.objects.filter(id=request.user.id).first().id

        category_code = request.data['category_code']
        data['category'] = Category.objects.get(code=category_code).id

        # data는 serializer를 거쳐
        serializer = self.get_seri(data=data)

        # 해당 결과가 유효하다면
        if serializer.is_valid():
            # DB에 저장 후 Response 객체에 data를 넣어 반환합니다. (status Code 201)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 그렇지 않다면 error와 함께 status Code 400을 반환합니다.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToggleLikeAPIView(APIView):
    # def get(self, request, post_pk):
        # post_pk로 Post 객체를 가져옵니다.
        # Post 객체의 like_users를 조회합니다.
        # request.user(요청을 보낸 사용자)가 like_users에 있다면 해당 사용자를 like_users에서 remove합니다 (좋아요 해제)
        # request.user(요청을 보낸 사용자)가 like_users에 없다면 해당 사용자를 like_users에 add합니다 (좋아요 등록)
        # 실행 결과에 따른 Response 객체 및 statusCode를 반환합니다. 
        # 200_OK, 401_UNAUTHORIZED 등
    pass