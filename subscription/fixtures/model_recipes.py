from datetime import date
from model_mommy.recipe import Recipe, foreign_key, related
from model_mommy import seq
from menu.fixtures.model_recipes import menu
from delivery.fixtures.model_recipes import delivery_schedule
from client.fixtures.model_recipes import profile
from subscription.models import Subscription, Order

subscription = Recipe(
    Subscription,
    days=28,
    menu=foreign_key(menu),
    delivery_schedule=foreign_key(delivery_schedule),
    weekdays_only=False
)

order = Recipe(
    Order,
    profile=foreign_key(profile),
    subscription=foreign_key(subscription),
    data_start=date(year=2020, month=1, day=1),
)
