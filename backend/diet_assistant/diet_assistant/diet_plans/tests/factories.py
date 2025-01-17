import factory

from diet_assistant.diet_plans.choices import CuisineType, MealType, Veganity
from diet_assistant.diet_plans.models import Day, DayMeal, DietPlan, Meal
from diet_assistant.users.tests.factories import UserFactory


class IngredientFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Ingredient {n}")

    class Meta:
        model = "diet_plans.Ingredient"
        django_get_or_create = ("name",)


class DietPlanFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    name = factory.Sequence(lambda n: f"Diet Plan {n}")

    class Meta:
        model = DietPlan
        django_get_or_create = ("name",)


class DayFactory(factory.django.DjangoModelFactory):
    diet_plan = factory.SubFactory(DietPlanFactory)
    day_number = factory.Sequence(lambda n: n)

    class Meta:
        model = Day
        django_get_or_create = ("day_number",)


class MealFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Meal {n}")
    description = factory.Sequence(lambda n: f"Description {n}")
    calories = factory.Faker("pyint")
    cuisine_type = CuisineType.ASIAN
    veganity = Veganity.VEGAN

    class Meta:
        model = Meal
        django_get_or_create = ("name",)

    @factory.post_generation
    def ingredients(self, create, extracted, **kwargs):
        if not extracted or not create:
            return
        for ingredient in extracted:
            self.ingredients.add(ingredient)


class DayMealFactory(factory.django.DjangoModelFactory):
    day = factory.SubFactory(DayFactory)
    meal = factory.SubFactory(MealFactory)
    meal_type = factory.Iterator(MealType.choices)

    class Meta:
        model = DayMeal
        django_get_or_create = ("meal_type",)
