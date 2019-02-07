from django.db import models
import re, bcrypt
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9+-_.]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, form_data):
        print("register success inside of your models!", form_data)
        errors = []

        if len(form_data["name"]) < 1:
            errors.append("name is required")
        elif len(form_data["name"]) < 2:
            errors.append("name must be 2 letters or longer")
        
        if len(form_data["alias"]) < 1:
            errors.append("alias is required")
        elif len(form_data["alias"]) < 2:
            errors.append("alias must be 2 letters or longer")

        if len(form_data["email"]) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(form_data["email"]):
            errors.append("Invalid Email")
        else:
            if len(User.objects.filter(email=form_data["email"].lower())) > 0:
                errors.append("Email already in use")

        if len(form_data["password"]) < 1:
            errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")

        if len(form_data["confirm"]) < 1:
            errors.append("Confirm Password is required")
        elif form_data["password"] != form_data["confirm"]:
            errors.append("Confirm Password must match Password")

        if len(form_data["dob"]) < 1:
            errors.append("Date of Birth is required")
        else:
            d = datetime.strptime(form_data["dob"], "%Y-%m-%d")
            if d > datetime.now():
                errors.append("The Date of Birth must be in the past")
        
        if len(errors) == 0:
            hashed_pw = bcrypt.hashpw(form_data["password"].encode(), bcrypt.gensalt())
            print(str(hashed_pw))
            user = User.objects.create(
                name = form_data["name"],
                alias = form_data["alias"],
                email = form_data["email"].lower(),
                password = hashed_pw,
                dob = form_data['dob'],
            )
            return (True, user)
        else:
            return (False, errors)

    def login(self, form_data):
        print("login success inside of your models!", form_data)

        errors = []

        if len(form_data["email"]) < 1:
            errors.append("Email is required")
        elif not EMAIL_REGEX.match(form_data["email"]):
            errors.append("Invalid Email")
        else:
            if len(User.objects.filter(email=form_data["email"].lower())) < 1:
                errors.append("Unknown email {}".format(form_data["email"]))

        if len(form_data["password"]) < 1:
            errors.append("Password is required")
        elif len(form_data["password"]) < 8:
            errors.append("Password must be 8 letters or longer")


        if len(errors) > 0:
            return (False, errors)

        user = User.objects.filter(email=form_data["email"].lower())[0]
        hashed_pw = user.password.split("'")[1]

        if bcrypt.checkpw(form_data["password"].encode(), hashed_pw.encode()):
            return (True, user)
        else:
            errors.append("Incorrect Password")
            return (False, errors)

    def friend(self, form_data):
        friended_user = User.objects.get(id=form_data["friended"])
        return True

class User(models.Model):
    name = models.CharField(max_length = 255)
    alias = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)

    friends = models.ManyToManyField("self", related_name="user_friends")
    
    dob = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
