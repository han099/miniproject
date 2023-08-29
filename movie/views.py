from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Q
from django.shortcuts import render, redirect
from .models import MovieInfo, MovieComment  # ,UserInfo
from django.core.paginator import Paginator
from django.db.models import Value
from django.db.models.functions import Coalesce
from django.utils import timezone


# Create your views here.

def movie_comment(request, movie_id):
    if request.method == "GET":
        print("comment GET")
        movieRating = \
            MovieComment.objects.filter(movie_id=movie_id).aggregate(average=Coalesce(Avg('rating'), Value(0.0)))[
                'average'] * 10
        movieInfo = MovieInfo.objects.get(movie_id=movie_id)

        comment_list = MovieComment.objects.filter(movie_id=movie_id).order_by('-update')
        page = request.GET.get('page', '1')
        paginator = Paginator(comment_list, 4)  # 페이지당 6개씩
        page_obj = paginator.get_page(page)

        context = {'movieInfo': movieInfo, 'comment_list': page_obj, 'movieRating': movieRating}
        return render(request, 'movie/movie-comment.html', context)
    if not request.user.is_authenticated:
        return redirect('/movie/list')
    if request.method == "POST":
        print("comment POST")

        movieInfo = MovieInfo.objects.get(movie_id=request.POST.get('movie_id', ''))
        # 받아온 값이 없을 때 나는 오류 예외 처리
        try:
            MovieComment.objects.get(user_id=request.user.id, movie_id=movieInfo.movie_id)

        except MovieComment.DoesNotExist:
            print("not yet")
            movieComment = MovieComment()
            movieComment.movie_id = movieInfo
            movieComment.username = request.user.username
            movieComment.user_id = request.user
            movieComment.rating = request.POST.get('rating', '')
            movieComment.comment = request.POST.get('comment', '')
            movieComment.save()
            return redirect('/movie/comment/' + str(request.POST.get('movie_id', '')))

        else:
            print("already")
            movieComment = MovieComment.objects.get(user_id=request.user.id, movie_id=movieInfo.movie_id)
            movieComment.username = request.user.username
            movieComment.rating = request.POST.get('rating', '')
            movieComment.comment = request.POST.get('comment', '')
            movieComment.save()
            return redirect('/movie/comment/' + str(request.POST.get('movie_id', '')))


def movie_delete(request, movie_id):
    if not request.user.is_superuser:
        return redirect('/movie/list')
    movieInfo = MovieInfo.objects.get(movie_id=movie_id)
    movieInfo.delete()
    return redirect('movie-list')


def movie_modify(request, movie_id):
    if not request.user.is_superuser:
        return redirect('/movie/list')
    if request.method == "GET":
        print('get')
        movieInfo = MovieInfo.objects.get(movie_id=movie_id)
        context = {'movieInfo': movieInfo}
        return render(request, 'movie/movie-modify.html', context)
    if request.method == "POST":
        print('post')
        print(movie_id)
        movieInfo = MovieInfo.objects.get(movie_id=movie_id)
        movieInfo.poster = request.FILES['poster']
        movieInfo.title = request.POST.get('title', '')
        movieInfo.director = request.POST.get('director', '')
        movieInfo.actors = request.POST.get('actors', '')
        movieInfo.genre = request.POST.get('genre', '')
        movieInfo.openingday = request.POST.get('openingday', '2000-02-02')
        movieInfo.trailer = request.POST.get('trailer', '')
        movieInfo.stillshot1 = request.FILES['stillshot1']
        movieInfo.stillshot2 = request.FILES['stillshot2']
        movieInfo.stillshot3 = request.FILES['stillshot3']
        movieInfo.save()
        return redirect('/movie/info/' + str(movieInfo.movie_id))


def movie_list(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    movie_list = MovieInfo.objects.all().order_by('-openingday')
    if kw:
        movie_list = movie_list.filter(
            Q(title__icontains=kw) |  # 제목 검색
            Q(director__icontains=kw) |  # 감독 검색
            Q(actors__icontains=kw) |  # 배우 검색
            Q(genre__icontains=kw)  # 장르 검색
        ).distinct()

    paginator = Paginator(movie_list, 6)  # 페이지당 12개씩
    page_obj = paginator.get_page(page)
    context = {'movie_list': page_obj, 'page': page, 'kw': kw}
    return render(request, 'movie/movie-list.html', context)


def movie_info(request, movie_id):
    print('info')
    movieInfo = MovieInfo.objects.get(movie_id=movie_id)
    movieRating = MovieComment.objects.filter(movie_id=movie_id).aggregate(average=Coalesce(Avg('rating'), Value(0.0)))[
                      'average'] * 10
    context = {'movieInfo': movieInfo, 'movieRating': movieRating}
    return render(request, 'movie/movie-info.html', context)


def movie_input(request):
    if not request.user.is_superuser:
        return redirect('/movie/list')
    if request.method == "GET":
        print('aa')
        return render(request, 'movie/movie-input.html')
    elif request.method == "POST":
        print('bb')
        movieInfo = MovieInfo()
        movieInfo.poster = request.FILES['poster']
        movieInfo.title = request.POST.get('title', '')
        movieInfo.director = request.POST.get('director', '')
        movieInfo.actors = request.POST.get('actors', '')
        movieInfo.genre = request.POST.get('genre', '')
        movieInfo.openingday = request.POST.get('openingday', '2000-02-02')
        movieInfo.trailer = request.POST.get('trailer', '')
        movieInfo.stillshot1 = request.FILES['stillshot1']
        movieInfo.stillshot2 = request.FILES['stillshot2']
        movieInfo.stillshot3 = request.FILES['stillshot3']
        movieInfo.save()
        return redirect('/movie/info/' + str(movieInfo.movie_id))
