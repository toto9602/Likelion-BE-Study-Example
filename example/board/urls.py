from django.urls import path


# /main 으로 시작하는 하위 url 설정
main_patterns = [
    path('posts/',), # 게시글 목록 조회, 게시글 생성
    path('posts/<int:post_pk>'), # 특정 게시글 수정, 삭제
    path('posts/<int:post_pk>/like') # 특정 게시글 좋아요 등록/해제
]