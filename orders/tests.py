from django.conf import settings
from django.test import TestCase, override_settings

from accounts.models import CustomUser
from .models import Station, Ingredient, StationIngredient
from .services import OrderService


class OrderServicePermissionsTests(TestCase):
    def test_admin_can_create_ingredient_order(self):
        admin = CustomUser.objects.create_user(
            username='admin-user',
            password='dummy-pass',
            role=CustomUser.Role.ADMIN,
        )
        self.assertTrue(OrderService.user_can_create_ingredient_order(admin))

    def test_orderer_can_create_ingredient_order(self):
        orderer = CustomUser.objects.create_user(
            username='orderer-user',
            password='dummy-pass',
            role=CustomUser.Role.ORDERER,
        )
        self.assertTrue(OrderService.user_can_create_ingredient_order(orderer))


class StationIngredientTests(TestCase):
    def test_str_includes_station_and_ingredient(self):
        station = Station.objects.create(name="Grill")
        ingredient = Ingredient.objects.create(name="Beef", unit="kg")
        link = StationIngredient.objects.create(station=station, ingredient=ingredient)
        self.assertEqual(str(link), "Grill + Beef")


class SecuritySettingsTests(TestCase):
    @override_settings(
        DEBUG=False,
        SECURE_SSL_REDIRECT=True,
        SECURE_HSTS_SECONDS=31536000,
        SECURE_HSTS_INCLUDE_SUBDOMAINS=True,
        SECURE_HSTS_PRELOAD=True,
        SESSION_COOKIE_SECURE=True,
        CSRF_COOKIE_SECURE=True,
    )
    def test_security_flags_enabled_in_prod(self):
        self.assertTrue(settings.SECURE_SSL_REDIRECT)
        self.assertGreater(settings.SECURE_HSTS_SECONDS, 0)
        self.assertTrue(settings.SESSION_COOKIE_SECURE)
        self.assertTrue(settings.CSRF_COOKIE_SECURE)
