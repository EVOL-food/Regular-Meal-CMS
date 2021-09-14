from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.utils.translation import gettext_lazy as _


class CustomImageStrategy(object):
    def on_existence_required(self, file):
        file.generate()

    def on_content_required(self, file):
        file.generate()

    def on_source_saved(self, file):
        file.generate()


class Ingredient(models.Model):
    title = models.CharField(max_length=60, default="",
                             verbose_name=_("Title"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Ingredient")
        verbose_name_plural = _("Ingredients")


class Photo(models.Model):
    title = models.CharField(max_length=60, default="",
                             verbose_name=_("Title"))
    image = models.ImageField(upload_to='menu/photos/', null=True, blank=True,
                              verbose_name=_("Image"))
    image_large = ImageSpecField(source='image', processors=[ResizeToFill(512, 512)], format='PNG',
                                 options={'quality': 70}, cachefile_strategy=CustomImageStrategy)
    image_medium = ImageSpecField(source='image', processors=[ResizeToFill(256, 256)], format='PNG',
                                  options={'quality': 70}, cachefile_strategy=CustomImageStrategy)
    image_small = ImageSpecField(source='image', processors=[ResizeToFill(128, 128)], format='PNG',
                                 options={'quality': 70}, cachefile_strategy=CustomImageStrategy)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Photo")
        verbose_name_plural = _("Photos")


class Category(models.Model):
    title = models.CharField(max_length=30, default="",
                             verbose_name=_("Title"))
    description = models.TextField(max_length=1000, default="",
                                   verbose_name=_("Description"))
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name=_("Photo"))
    slug = models.SlugField(max_length=30, unique=True,
                            default="", blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _('Categories')


class Dish(models.Model):
    title = models.CharField(max_length=60, default="", verbose_name=_("Title"))
    description = models.TextField(default="", max_length=1000,
                                   verbose_name=_("Description"))
    ingredients = models.ManyToManyField(to=Ingredient,
                                         verbose_name=_("Ingredients"),
                                         related_name='dishes')
    calories = models.PositiveIntegerField(default=0,
                                           verbose_name=_("Calories"))
    meal_of_the_day = models.PositiveIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        verbose_name=_("Meal of the day"))
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name=_("Photo"))
    slug = models.SlugField(max_length=60, unique=True,
                            default="", blank=True, null=True)

    def __str__(self):
        return self.title

    @property
    def get_ingredients_list(self):
        return [ingredient["title"] for ingredient in self.ingredients.values()]

    class Meta:
        verbose_name = _("Dish")
        verbose_name_plural = _("Dishes")


class DailyMeal(models.Model):
    title = models.CharField(default="", max_length=100,
                             verbose_name=_("Title"))
    dish_1 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='breakfast',
                               verbose_name=_("Breakfast"))
    dish_2 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='brunch',
                               verbose_name=_("Brunch"))
    dish_3 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='lunch',
                               verbose_name=_("Lunch"))
    dish_4 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='dinner',
                               verbose_name=_("Dinner"))
    dish_5 = models.ForeignKey(Dish, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name='supper',
                               verbose_name=_("Supper"))

    calories = models.PositiveIntegerField(default=0,
                                           verbose_name=_("Calories"))

    def __str__(self):
        return self.title

    @property
    def get_all_dishes(self):
        dishes = [self.dish_1, self.dish_2,
                  self.dish_3, self.dish_4, self.dish_5]
        return dishes

    class Meta:
        verbose_name = _("Daily meal")
        verbose_name_plural = _("Daily meals")


class Menu(models.Model):
    title = models.CharField(max_length=30,
                             verbose_name=_('Title'))
    description = models.TextField(max_length=1000, default="",
                                   verbose_name=_('Description'))
    calories_daily = models.PositiveIntegerField(default=0,
                                                 verbose_name=_('Calories average'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 verbose_name=_('Category'))
    photo = models.ForeignKey(Photo, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name=_('Photo'))
    slug = models.SlugField(max_length=30, unique=True, default="", blank=True, null=True)

    price_auto = models.BooleanField(default=True,
                                     verbose_name=_('Auto price'))
    price_daily = models.DecimalField(default=0, max_digits=5,
                                      decimal_places=2,
                                      verbose_name=_('Daily costs'))
    price_weekly = models.DecimalField(default=0, max_digits=7,
                                       decimal_places=2,
                                       verbose_name=_('Weekly costs'))
    price_monthly = models.DecimalField(default=0, max_digits=10,
                                        decimal_places=2,
                                        verbose_name=_('Monthly costs'))

    day_1 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="monday",
                              verbose_name=_('Monday'))
    day_2 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="tuesday",
                              verbose_name=_("Tuesday"))
    day_3 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="wednesday",
                              verbose_name=_("Wednesday"))
    day_4 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="thursday",
                              verbose_name=_("Thursday"))
    day_5 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="friday",
                              verbose_name=_("Friday"))
    day_6 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="saturday",
                              verbose_name=_("Saturday"))
    day_7 = models.ForeignKey(DailyMeal, on_delete=models.CASCADE,
                              related_name="sunday",
                              verbose_name=_("Sunday"))

    def __str__(self):
        return self.title

    @property
    def get_all_days(self):
        days = [self.day_1, self.day_2, self.day_3,
                self.day_4, self.day_5, self.day_6, self.day_7]
        return days

    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menus")


class IngredientDishesProxy(Dish.ingredients.through):
    class Meta:
        proxy = True
        app_label = 'menu'
        auto_created = True

    def __str__(self):
        self._meta.get_field('dish').verbose_name = _("Dish")
        return self.dish.title
