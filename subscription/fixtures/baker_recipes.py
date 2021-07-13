from datetime import date
from model_bakery.recipe import Recipe, foreign_key
from subscription.models import Subscription, Order
from menu.fixtures.baker_recipes import menu
from delivery.fixtures.baker_recipes import delivery_schedule
from client.fixtures.baker_recipes import client

subscription = Recipe(
    Subscription,
    days=28,
    menu=foreign_key(menu),
    delivery_schedule=foreign_key(delivery_schedule),
    weekdays_only=False
)

order = Recipe(
    Order,
    profile=foreign_key(client),
    subscription=foreign_key(subscription),
    data_start=date(year=2020, month=1, day=1),
)
