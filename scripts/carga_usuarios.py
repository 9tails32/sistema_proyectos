from django.contrib.auth.models import User

for i in range(1,10):
    user = User.objects.create_user('user' + str(i),email=None,password='password' + str(i))
