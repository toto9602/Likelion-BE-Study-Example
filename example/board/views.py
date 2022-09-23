from rest_framework.views import APIView

from .models import Post

# APIView를 상속받아 CBV로 작성합니다.
# APIView를 상속받은 클래스 안에 request method에 맞는 함수들을 정의해주면
# 각각의 요청은 request method 이름에 맞게 구분되어 그에 맞는 결과를 반환합니다.
class PostListAPIView(APIView):
    # URL : board/posts 
    # HTTP Method : GET
    def get(self, request):
        posts = Post.objects.all()




