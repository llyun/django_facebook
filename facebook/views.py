from django.shortcuts import render, redirect
from facebook.models import Article
from facebook.models import Comment

def daegyunlim(request):
    return render(request, 'daegyunlim.html')
count=0
def play(request):

    diary = ['승은님 생일 축하해요 - 수요일','축하해주세요 - 헌준님','헌영님도요']

    a = "daegyunlim"

    age = 18
    if age > 19:
        status = '성인'
    else:
        status = '미성년자'


    global count
    count = count + 1

    return render(request, 'play.html', { 'diary: diary'})

# 첫 페이지 = 뉴스피드 페이지 역할
def newsfeed(request):
    #연결 작업을 할 예정
    articles = Article.objects.all()

    return render(request, 'article_list.html', {'articles': articles})

# detail 작업
def article_detail(request, pk):
    #pk 글을 불러와서 detail.html로 보내주기
    post = Article.objects.get(pk=pk)

    return render(request, 'article_details.html', { 'feed':post })

def detail_article(request, pk):
    article = Article.objects.get(pk=pk)

    if request.method == 'POST': #new comment
        Comment.objects.create(
            article=article,
            author=request.POST.get('author'),
            text=request.POST.get('text'),
            password=request.POST.get('password')
        )

        return redirect(f'/article/{ article.pk }')

    return render(request, 'article_details.html', {'feed': article})

# article_new 도전 작업
def article_new(request):
    if request.method == 'POST': # 게시를 눌렀을때만 실행됨
        new_article = Article.objects.create(
            author=request.POST.get('author'),
            title=request.POST.get('title'),
            text=request.POST.get('text'),
            password=request.POST.get('password')
        )

        return redirect(f'/article/{ new_article.pk }')

    return render(request, 'article_new.html')

# article_new 도전 작업
def help(request):

    return render(request, 'help.html')

def remove_comment(request, pk):
    comment = Comment.objects.get(pk=pk)

    if request.method == 'POST':
        password = request.POST.get('password')

        if password == comment.password:
            comment.delete()
            return redirect(f'/article/{ comment.article.pk }')
        else:
            return redirect('/fail/')

    return render(request, 'article_remove.html', { 'show_message': comment.text })