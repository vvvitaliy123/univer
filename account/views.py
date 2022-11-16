from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate 
from django.core.mail import send_mail
from hashlib import md5


def reg(request):
    if request.method == 'GET':
        return render(request, 'account/reg.html')
    elif request.method =='POST':
        # 1. Зчитуємо із форми реєстрації дані:
        login = request.POST.get('login')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        email = request.POST.get('email')

        # 2. Сценарій реєстрації
        report = dict()
        passw = md5(pass1.encode('utf-8')).hexdigest()
        new_user = User.objects.create_user(login, email, passw)
        if new_user is None:
            report['mess'] = 'У реєстрації відмовлено!'
        else:
            report['mess'] = 'Ви успішно зареєстровані!'
            # 3. Готуємо повідомлення на пошту користувача для підтвердження реєстрації!
            url = f'http://localhost:8000/account/confirm?email={email}'
            subject = 'Підтвердження реєстарції на сайті Univer'
            body = f"""
                <hr />
                <h3>Для підтвердження реєстрації перейдіть за посиланням</h3>
                <h4>
                    <a href="{url}">{url}</a>
                </h4>   
                <hr />
            """                    
        return render(request, 'account/reg_res.html', context=report)


def confirm(request):
    # Зчитуємо емайл, від якого прийшло підтвердження
    email = request.GET.get('email')

    # Знаходимо користувача із даним E-Mail:
    user = User.objects.filter(email=email)

    # Додаємо користувача до групи ConfirmedUser
    group = User.groups.filter(name='ConfirmedUser')
    User.groups.add(group)

    # Група в адмінці

    return render(request, 'account/confirm.html')

def entry(request):
    return render(request, 'account/entry.html')
    

def exit(request):
    return render(request, 'account/exit.html')

def profile(request):
    return render(request, 'account/profile.html')
    

def reset(request):
    return render(request, 'account/reset.html')
