from model_bakery.recipe import Recipe
from django.contrib.auth.models import User
from client.models import Client

user = Recipe(
    User
)

client = Recipe(
    Client,
    first_name='Mario',
    phone_number='hello954507777'
)
