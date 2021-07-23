from django.contrib.auth.models import User
from model_mommy.recipe import Recipe, foreign_key, related
from model_mommy import seq
from client.models import Profile

user = Recipe(
    User,
    username=seq("username"),
    email="email@email.com"
)

profile = Recipe(
    Profile,
    first_name=seq("Name"),
    last_name=seq("Surname"),
    phone_number=seq("No+38099451780"),
    address=seq("Address"),
    gender=1
)
