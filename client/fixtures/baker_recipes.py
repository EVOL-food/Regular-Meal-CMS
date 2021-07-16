from model_bakery.recipe import Recipe
from django.contrib.auth.models import User
from client.models import Profile

user = Recipe(
    User
)

client = Recipe(
    Profile,
    first_name='Mario',
    phone_number='hello954507777'
)
