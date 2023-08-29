from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.core.paginator import Paginator




# Create your views here.
def board(request):
    page_number = request.GET.get('page', '1')
    print('pass')
    kw = request.GET.get('blog_kw', '')  # 검색어
    posts = Post.objects.all()
    if kw:
        posts = posts.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(content__icontains=kw)   # 내용 검색
        ).distinct()
    paginator = Paginator(posts, 10)  # 한 페이지에 10개씩 표시
    page_obj = paginator.get_page(page_number)
    context={'posts': page_obj,'page': page_number, 'kw': kw}


    return render(request, 'board/board.html',context)

@login_required
def delete_post(request, post_num):
    print('delete')
    posts = Post.objects.get(post_num=post_num)
    posts.delete()
    return redirect('board')

@login_required
def modify_post(request, post_num):
    posts = Post.objects.get(post_num=post_num)
    if request.user != posts.writer:
        return redirect('/board')
    if request.method == "GET":
        print("get")
        posts = Post.objects.get(post_num=post_num)
        context = {'posts': posts}
        return render(request, 'board/post_modify.html', context)
    elif request.method == "POST":
        print("post")
        # POST 요청 처리
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')

        if title and content:  # 제목과 내용이 모두 존재하는 경우에만 저장
            posts = Post.objects.get(post_num=post_num)
            posts.title = request.POST.get('title', '')
            posts.content = request.POST.get('content', '')
            posts.save()
            return redirect('/board/detail/' + str(posts.post_num))
        else:
            posts = Post.objects.get(post_num=post_num)
            error_message = "제목과 내용을 모두 입력해주세요."
            context = {'posts': posts,'error_message':error_message}
            return render(request, 'board/post_modify.html', context)


@login_required
def create_post(request):
    if request.method == "GET":
        print("get")
        return render(request, 'board/post_create.html')
    elif request.method == "POST":
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')

        if title and content:  # 제목과 내용이 모두 존재하는 경우에만 저장
            post = Post(title=title, content=content, writer=request.user)
            post.save()
            return redirect('board')
        else:
            error_message = "제목과 내용을 모두 입력해주세요."
            return render(request, 'board/post_create.html', {'error_message': error_message})

def detail_post(request, post_num):
    print('detail')
    # 게시글 상세 페이지 뷰
    post = get_object_or_404(Post, post_num=post_num)
    comments = Comment.objects.filter(post=post)
    return render(request, 'board/post_detail.html', {'post': post, 'comments': comments})

@login_required()
def create_comment(request, post_num):
    # 댓글 등록 뷰
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            post = get_object_or_404(Post, post_num=post_num)
            comment = Comment.objects.create(content=content, writer=request.user, post=post)
            return redirect('post-detail', post_num=post_num)
    # 댓글이 생성된 후에 댓글 목록을 다시 조회하여 템플릿으로 넘기기

@login_required()
def delete_comment(request, post_num, comment_id):
    # 댓글 삭제 뷰
    print('delete')
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('post-detail', post_num=post_num)
