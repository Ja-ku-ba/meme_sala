from itertools import chain

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserForm, LoginForm, PostForm
from .models import Account, Post, Like, Dislike, Coment
# Create your views here.
def home(request):
    posts = Post.objects.all()
    context = {'posts':posts}
    return render(request, 'meme/home.html', context)



def register(request):
    form = UserForm
    status = 'Zarejestruj'
    context = {'form':form, 'status':status}
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            email = form.cleaned_data.get('email').lower()
            if Account.objects.filter(email=email).exists():
                messages.danger(request, "Użytkownik z podnaym adresem email już istnieje, spróbuj się zalogować.")
                return redirect('register')
            form.save(commit=True)
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            
            messages.success(request, f"Zalogowano pomyślnie, witaj {account.username}")
            return redirect('home')
        else:
            email = request.POST.get('email').lower()
            if Account.objects.filter(email=email).exists():
                messages.danger(request, "Użytkownik z podnaym adresem email już istnieje, spróbuj się zalogować.")
            
            username = request.POST.get('username')
            if Account.objects.filter(username=username).exists():
                messages.danger(request, "Użytkownik o podanej nazwie już istnieje, spróbuj innej.")
            else:
                messages.danger(request, "Sprawdź czy wprowadzne hasła są takie same.")
            return redirect('register')

    return render(request, 'meme/login_register.html', context)



def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    status = 'Zaloguj'
    form = LoginForm
    context = {'form':form, 'status':status}
    if request.method == 'POST':
        email = request.POST.get("email")
        raw_password = request.POST.get("password")

        checker = False

        try:
            user = Account.objects.get(email=email)
        except:
            checker = True
            
        user = authenticate(email=email, password=raw_password)

        if checker is True or user is None:
            messages.danger(request, 'Błędna nazwa użytkowinka lub hasło')
        else:
            login(request, user)
            messages.success(request, f"Zalogowano pomyślnie, witaj {user.username}")
            return redirect('home')
    return render(request, 'meme/login_register.html', context)




def logout_user(request):
    logout(request)
    messages.info(request, "Wylogowano pomyślnie.")
    return redirect('home')



def post_add(request):
    form = PostForm
    context = {'form':form}
    if request.method == "POST":
        img = request.FILES.get('image')
        if img is None:
            messages.info(request, "Aby dodać post, muszisz dodać mema")
            return redirect('post_add')
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            new_post = Post.objects.create(
                title = request.POST.get('title'),
                body = request.POST.get('body'),
                owner = request.user,
            )
            new_post.image = img
            new_post.save()
            messages.success(request, "Post został dodany")

            return redirect('post', new_post.id)
        messages.info(request, "Coś poszło nie tak")
        return redirect('home')
    return render(request, 'meme/post_add.html', context)



def post(request, pk):
    # if user create random link
    try:
        post_req = Post.objects.get(id=pk)
        coments = Coment.objects.filter(post=post_req)
    except:
        messages.info(request, "Post nie istnieje")
        return redirect('home')

    # add coment function
    if request.method == "POST":
        if request.POST.get('coment'):
            body = request.POST.get("body")
            body = body[:256]
            Coment.objects.create(
                post = post_req,
                body = body,
                owner = request.user
            )

            return redirect('post', post_req.id)
    if request.user.is_authenticated:
        like_status = Like.objects.filter(post=post_req, owner=request.user).exists()
        dislike_status = Dislike.objects.filter(post=post_req, owner=request.user).exists()
    else:
        like_status = False
        dislike_status = False
    context = {'post':post_req, 'coments':coments, 'like_status':like_status, 'dislike_status':dislike_status}
    return render(request, 'meme/post.html', context)



def post_delete(request, pk):
    try:
        post_req = Post.objects.get(id=pk)
    except:
        messages.info(request, "Coś poszło nie tak")
        return redirect('home')
    if request.user == post_req.owner:
        if request.method == "POST":
            post_req.delete()
            messages.info(request, "Post został pomślnie usunięty")
            return redirect("home")
    else:
        messages.info(request, "Nie masz uprawnień do wykonania tej czynności")
        return redirect("home")
    context = {'post':post_req}
    return render(request, 'meme/post_delete.html', context)



def like(request, pk):
    # if user create random link with post id that does not exists
    try:
        post_req = Post.objects.get(id=pk)
    except:
        messages.info(request, "Nie można wykonać tej czynności")
        return redirect("home")
    
    # check if like model exists
    try:
        model = Like.objects.get(post=post_req)
        # exists so user want to unlike
        model.delete()
        post_req.interactions -= 1
    except:
        model = Like.objects.create(
            post = post_req,
            owner = request.user
        )
        model.save()
        post_req.interactions += 1

    # user can like or dislike, delete one status if user change opinion
    dislike_status = Dislike.objects.filter(post=post_req, owner=request.user).exists()
    if dislike_status is True:
        Dislike.objects.get(post=post_req, owner=request.user).delete()
        dislike_status = False

        # change iterraction staus to undislike
        post_req.interactions += 1

    post_req.save()        
    return redirect('post', post_req.id)



def dislike(request, pk):
    # if user create random link with post id that does not exists
    try:
        post_req = Post.objects.get(id=pk)
    except:
        messages.info(request, "Nie można wykonać tej czynności")
        return redirect("home")
    
    # check if dislike model exists
    try:
        model = Dislike.objects.get(post=post_req)
        # exists so user want to undislike
        model.delete()
        post_req.interactions += 1
    except:
        model = Dislike.objects.create(
            post = post_req,
            owner = request.user
        )
        model.save()
        post_req.interactions -= 1

    # user can like or dislike, delete one status if user change opinion
    like_status = Like.objects.filter(post=post_req, owner=request.user).exists()
    if like_status is True:
        Like.objects.get(post=post_req, owner=request.user).delete()
        like_status = False
        # change iterraction staus to unlike
        post_req.interactions -= 1

    post_req.save()
    return redirect('post', post_req.id)



def coment_delete(request, pk):
    # if user creates own link
    try:
        coment = Coment.objects.get(id=pk)
    except:
        messages.info(request, "Nie można wykonać tej czynności")
        return redirect("home")
    
    if request.user == coment.owner:
        coment.delete()
        messages.info(request, "Komenterz usunięty")
    else:
        messages.info(request, "Nie można wykonać tej czynności")
        return redirect("home")

    return redirect("post", coment.post.id)


def user_page(request, pk):
    # if user create random link
    try:
        user = Account.objects.get(id=pk)
    except:
        messages.info(request, "Nie można wykonać tej czynności")
        return redirect("home.html")

    user_posts = Post.objects.filter(owner=user)

    context = {'user':user, 'posts':user_posts}
    return render(request, 'meme/user_page.html', context)


def user_interactions(request):
    likes = Like.objects.filter(owner=request.user)
    dislikes = Dislike.objects.filter(owner=request.user)
    coments = Coment.objects.filter(owner=request.user)

    interactions = chain(likes, dislikes, coments)
    context = {'posts':interactions}
    return render(request, 'meme/user_interactions.html', context)

def user_notifications(request):
    posts = Post.objects.filter(owner=request.user)
    likes = Like.objects.all()
    dislikes = Dislike.objects.all()
    coments = Coment.objects.all()

    # to optimalize
    interactions = chain(likes, dislikes, coments)
    context = {'posts':posts, 'interactions':interactions}
    return render(request, 'meme/user_notifications.html', context)