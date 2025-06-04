from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


def init_db_users():
    try:
        if User.objects.all().count() > 10:
            print('User table not empty!')
            return
        
        users_data = [
            {
                "username": "alice",
                "email": "alice@example.com",
                "password": "alice1234",
                "plan": User.Plan.FREE,
            },
            {
                "username": "bob",
                "email": "bob@example.com",
                "password": "bobsecure",
                "plan": User.Plan.PRO,
                "filter_date_from": date(2024, 1, 1),
                "filter_date_to": date(2024, 12, 31),
            },
            {
                "username": "carol",
                "email": "carol@example.com",
                "password": "carolpw",
                "plan": User.Plan.FREE,
            },
            {
                "username": "dave",
                "email": "dave@example.com",
                "password": "davepass",
                "plan": User.Plan.PRO,
            },
            {
                "username": "eve",
                "email": "eve@example.com",
                "password": "evesecret",
                "plan": User.Plan.PRO,
            },
        ]


        for data in users_data:
            password = data.pop("password")
            user = User(**data)
            user.set_password(password)
            user.save()
        
        print(f'{len(users_data)} user added!')

    except Exception as e:
        print('Error while filling DB with users: ' + str(e))

from django.contrib.auth.models import Group, Permission

def init_db_groups():
    try:
        if Group.objects.count() > 0:
            print("Group table not empty!")
            return

        groups_data = [
            {
                "name": "Ferrari",
                "permissions": [],  
            },
            {
                "name": "Unimore",
                "permissions": [],
            },
        ]

        for group_data in groups_data:
            perms = group_data.pop("permissions", [])
            group = Group.objects.create(**group_data)
            if perms:
                group.permissions.set(Permission.objects.filter(codename__in=perms))

        print(f"{len(groups_data)} groups created!")

    except Exception as e:
        print("Error while filling DB with groups: " + str(e))
