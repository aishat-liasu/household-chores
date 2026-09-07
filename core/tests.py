from django.contrib.staticfiles import finders
from django.test import TestCase


class HealthCheckTests(TestCase):
    def test_health_endpoint_returns_200(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)


class HomePageTests(TestCase):
    def test_home_returns_200(self):
        self.assertEqual(self.client.get("/").status_code, 200)

    def test_home_shows_header(self):
        self.assertContains(self.client.get("/"), "Household Chores")

    def test_home_references_htmx(self):
        self.assertContains(self.client.get("/"), "htmx.min.js")


class HtmxFragmentTests(TestCase):
    def test_ping_returns_fragment(self):
        response = self.client.get("/ping/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "pong")


class StaticAssetTests(TestCase):
    def test_css_is_findable(self):
        self.assertIsNotNone(finders.find("css/app.css"))

    def test_htmx_is_findable(self):
        self.assertIsNotNone(finders.find("vendor/htmx.min.js"))


from django.contrib.auth import get_user_model


class UserRoleTests(TestCase):
    def test_default_role_is_child(self):
        user = get_user_model().objects.create_user("kid", password="pw")
        self.assertEqual(user.role, "child")
        self.assertTrue(user.is_child)
        self.assertFalse(user.is_parent)

    def test_parent_role_helpers(self):
        user = get_user_model().objects.create_user("mum", password="pw", role="parent")
        self.assertTrue(user.is_parent)
        self.assertFalse(user.is_child)


class AuthTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            "mum", password="secret123", role="parent"
        )

    def test_login_page_renders(self):
        r = self.client.get("/login/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "Sign in")

    def test_valid_login_redirects_to_dashboard(self):
        r = self.client.post("/login/", {"username": "mum", "password": "secret123"})
        self.assertRedirects(r, "/dashboard/")

    def test_invalid_login_shows_error(self):
        r = self.client.post("/login/", {"username": "mum", "password": "nope"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "didn't match")

    def test_protected_page_redirects_anonymous(self):
        r = self.client.get("/dashboard/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login/", r.url)

    def test_logout_ends_session(self):
        self.client.login(username="mum", password="secret123")
        r = self.client.post("/logout/")
        self.assertEqual(r.status_code, 302)
        self.assertEqual(self.client.get("/dashboard/").status_code, 302)


class MemberSignupTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.parent = U.objects.create_user("mum", password="secret123", role="parent")
        self.child = U.objects.create_user("kid", password="secret123", role="child")

    def test_parent_can_create_member_who_can_log_in(self):
        self.client.login(username="mum", password="secret123")
        r = self.client.post("/members/new/", {
            "username": "junior", "role": "child",
            "password1": "Sup3rSecret!", "password2": "Sup3rSecret!"})
        self.assertRedirects(r, "/dashboard/")
        U = get_user_model()
        self.assertTrue(U.objects.filter(username="junior", role="child").exists())
        self.assertTrue(self.client.login(username="junior", password="Sup3rSecret!"))

    def test_duplicate_username_rejected(self):
        self.client.login(username="mum", password="secret123")
        r = self.client.post("/members/new/", {
            "username": "kid", "role": "child",
            "password1": "Sup3rSecret!", "password2": "Sup3rSecret!"})
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "already exists")

    def test_child_cannot_create_member(self):
        self.client.login(username="kid", password="secret123")
        self.assertEqual(self.client.get("/members/new/").status_code, 403)

    def test_anonymous_redirected_to_login(self):
        r = self.client.get("/members/new/")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login/", r.url)


from core.models import Household


class HouseholdTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.hA = Household.objects.create(name="Alpha")
        self.hB = Household.objects.create(name="Beta")
        self.pA = U.objects.create_user("mumA", password="secret123", role="parent", household=self.hA)
        self.cA = U.objects.create_user("kidA", password="secret123", role="child", household=self.hA)
        self.pB = U.objects.create_user("mumB", password="secret123", role="parent", household=self.hB)

    def test_user_belongs_to_one_household(self):
        self.assertEqual(self.pA.household, self.hA)
        self.assertIn(self.cA, list(self.hA.members.all()))

    def test_members_page_scoped_to_own_household(self):
        self.client.login(username="mumA", password="secret123")
        r = self.client.get("/household/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "kidA")
        self.assertNotContains(r, "mumB")
