from django.shortcuts import render,redirect
from .forms import LoginForm,RegisterForm,CustomUserChangeForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import PasswordResetForm
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
import random,string

# Create your views here.
def main(request):
    return render(request,'base.html')


def sign_in(request):
    if request.method == 'GET':
        remembered_username = request.session.get('remembered_username', '')
        #form = LoginForm()
        return render(request,'account/auth-login-basic.html',{'remembered_username':remembered_username})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if not form.is_valid():
            print(form.errors)
        elif form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_id = request.POST.get('remember-id')
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request,user)
                response = redirect('movie-list')
                if remember_id:
                    response.set_cookie('remembered_username',username,max_age=(3600*24*1))
                else:

                    response.delete_cookie('remembered_username')
                messages.success(request,f'{username.title()}님 로그인을 환영합니다!')
                return response
            else:
                messages.error(request, f'유효하지 않은 id나 password 입니다')
                return render(request, 'account/auth-login-basic.html')
        else:
            messages.error(request,f'유효하지 않은 id나 password 입니다')
            return render(request, 'account/auth-login-basic.html')
def edit_profile(request):
    if request.user.is_authenticated:
        saved_user_profile = request.session.get('saved_user_profile', {})
        initial_data = {
            'lastName': saved_user_profile.get('lastName', ''),
            'firstName': saved_user_profile.get('firstName', ''),
            'phoneNumber': saved_user_profile.get('phoneNumber', ''),
            'state': saved_user_profile.get('state', ''),
            'address': saved_user_profile.get('address', ''),
            'Janre': saved_user_profile.get('Janre', ''),
            'language': saved_user_profile.get('language', ''),
            'gender': saved_user_profile.get('gender', ''),
        }
        form = CustomUserChangeForm(initial=initial_data, instance=request.user)
        return render(request, 'account/pages-account-settings-account.html',
                      {'form': form})
    else:
        messages.success(request, f'정보 수정을 하려면 로그인을 하셔야 합니다')
        return render(request, 'account/auth-login-basic.html')

def sign_out(request):
    logout(request)
    messages.success(request,f'로그아웃 성공')
    return redirect(reverse('login'))


def sign_up(request):
    if request.method =='GET':
        #form = RegisterForm()
        return render(request,'account/auth-register-basic.html')#,{'form':form})
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,"회원가입 성공")
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request,user)
                return redirect('movie-list')
        else:
            form =RegisterForm()
            print('error')
        return render(request,'account/auth-register-basic.html',{'form':form})

def forgot(request):
    if request.method =='GET':
        return render(request,'account/auth-forgot-password-basic.html')
    if request.method =='POST':
        form = PasswordResetForm(request.POST)
        if not form.is_valid():
            print(form.errors)
        elif form.is_valid():
            form.save(
                request=request,
                from_email='cinester@naver.com',
                email_template_name='account/auth-password-reset.html'
            )
        else:
            form = PasswordResetForm()
        return render(request,'account/auth-forgot-password-basic.html')
@require_POST
def delete_user(request):
    if request.user.is_authenticated and request.POST.get("accountActivation"):
        request.user.delete()
        JsonResponse({"success": True})
        messages.success(request, '회원탈퇴가 완료되었습니다.')
        return redirect('main')
    else:
        JsonResponse({"success": False})

    return render(request,'account/pages-account-settings-connections.html')

@login_required()
def save_edit_profile(request):
    if request.method =='POST':
        form = CustomUserChangeForm(request.POST,instance=request.user)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            request.session['saved_user_profile'] = form.cleaned_data
            messages.success(request, '회원정보가 수정되었습니다.')
            return redirect('edit-profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request,'account/pages-account-settings-account.html',{'form':form})