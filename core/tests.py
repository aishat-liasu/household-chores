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


from django.core.exceptions import ValidationError

from core.models import Chore


class ChoreModelTests(TestCase):
    def setUp(self):
        self.h = Household.objects.create(name="Home")
        self.kid = get_user_model().objects.create_user(
            "kid2", password="x", role="child", household=self.h
        )

    def test_create_chore_defaults(self):
        c = Chore.objects.create(
            title="Dishes", assignee=self.kid, household=self.h, points=5
        )
        self.assertEqual(c.status, Chore.Status.ASSIGNED)
        self.assertEqual(c.recurrence, Chore.Recurrence.NONE)
        self.assertEqual(c.points, 5)

    def test_points_cannot_be_negative(self):
        c = Chore(title="Bad", assignee=self.kid, household=self.h, points=-1)
        with self.assertRaises(ValidationError):
            c.full_clean()


class ChoreCreateTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.h = Household.objects.create(name="Home")
        self.other = Household.objects.create(name="Other")
        self.parent = U.objects.create_user("mumC", password="secret123", role="parent", household=self.h)
        self.child = U.objects.create_user("kidC", password="secret123", role="child", household=self.h)
        self.outsider = U.objects.create_user("kidO", password="secret123", role="child", household=self.other)

    def test_parent_creates_assigned_chore(self):
        self.client.login(username="mumC", password="secret123")
        r = self.client.post("/chores/new/", {
            "title": "Dishes", "description": "", "points": 5,
            "assignee": self.child.id, "recurrence": "none"})
        self.assertRedirects(r, "/dashboard/")
        c = Chore.objects.get(title="Dishes")
        self.assertEqual(c.assignee, self.child)
        self.assertEqual(c.status, "assigned")
        self.assertEqual(c.household, self.h)

    def test_assignee_limited_to_household(self):
        self.client.login(username="mumC", password="secret123")
        r = self.client.post("/chores/new/", {
            "title": "X", "description": "", "points": 1,
            "assignee": self.outsider.id, "recurrence": "none"})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Chore.objects.filter(title="X").exists())

    def test_child_cannot_create(self):
        self.client.login(username="kidC", password="secret123")
        self.assertEqual(self.client.get("/chores/new/").status_code, 403)

    def test_invalid_input_rejected(self):
        self.client.login(username="mumC", password="secret123")
        r = self.client.post("/chores/new/", {
            "title": "", "description": "", "points": 5,
            "assignee": self.child.id, "recurrence": "none"})
        self.assertEqual(r.status_code, 200)
        self.assertFalse(Chore.objects.filter(title="").exists())


class MyChoresTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.h = Household.objects.create(name="Home")
        self.a = U.objects.create_user("aa", password="secret123", role="child", household=self.h)
        self.b = U.objects.create_user("bb", password="secret123", role="child", household=self.h)
        Chore.objects.create(title="A-chore", assignee=self.a, household=self.h, points=3)
        Chore.objects.create(title="B-chore", assignee=self.b, household=self.h, points=4)

    def test_member_sees_only_their_chores(self):
        self.client.login(username="aa", password="secret123")
        r = self.client.get("/chores/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "A-chore")
        self.assertNotContains(r, "B-chore")

    def test_empty_state(self):
        get_user_model().objects.create_user("cc", password="secret123", role="child", household=self.h)
        self.client.login(username="cc", password="secret123")
        self.assertContains(self.client.get("/chores/"), "no chores")


class MarkDoneTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.h = Household.objects.create(name="Home")
        self.a = U.objects.create_user("aa2", password="secret123", role="child", household=self.h)
        self.b = U.objects.create_user("bb2", password="secret123", role="child", household=self.h)
        self.chore = Chore.objects.create(title="Dishes", assignee=self.a, household=self.h, points=5)

    def test_owner_marks_done_without_points(self):
        self.client.login(username="aa2", password="secret123")
        r = self.client.post(f"/chores/{self.chore.id}/done/")
        self.assertEqual(r.status_code, 200)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, "done")
        self.assertNotEqual(self.chore.status, "verified")

    def test_non_owner_denied(self):
        self.client.login(username="bb2", password="secret123")
        r = self.client.post(f"/chores/{self.chore.id}/done/")
        self.assertEqual(r.status_code, 403)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, "assigned")

    def test_marking_verified_is_noop(self):
        self.chore.status = "verified"
        self.chore.save()
        self.client.login(username="aa2", password="secret123")
        r = self.client.post(f"/chores/{self.chore.id}/done/")
        self.assertEqual(r.status_code, 200)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, "verified")


class VerifyTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.h = Household.objects.create(name="Home")
        self.parent = U.objects.create_user("mumV", password="secret123", role="parent", household=self.h)
        self.child = U.objects.create_user("kidV", password="secret123", role="child", household=self.h)
        self.chore = Chore.objects.create(
            title="Sweep", assignee=self.child, household=self.h, points=7, status="done")

    def test_parent_verifies_awards_points_once(self):
        self.client.login(username="mumV", password="secret123")
        r = self.client.post(f"/chores/{self.chore.id}/verify/")
        self.assertEqual(r.status_code, 200)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, "verified")
        self.assertEqual(self.child.verified_points, 7)
        # re-verify must not double-count
        self.client.post(f"/chores/{self.chore.id}/verify/")
        self.assertEqual(self.child.verified_points, 7)

    def test_child_cannot_verify(self):
        self.client.login(username="kidV", password="secret123")
        r = self.client.post(f"/chores/{self.chore.id}/verify/")
        self.assertEqual(r.status_code, 403)
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, "done")

    def test_verify_requires_done_state(self):
        self.chore.status = "assigned"
        self.chore.save()
        self.client.login(username="mumV", password="secret123")
        self.client.post(f"/chores/{self.chore.id}/verify/")
        self.chore.refresh_from_db()
        self.assertEqual(self.chore.status, "assigned")
        self.assertEqual(self.child.verified_points, 0)

    def test_pending_list_shows_done_chore(self):
        self.client.login(username="mumV", password="secret123")
        r = self.client.get("/chores/verify/")
        self.assertContains(r, "Sweep")


from datetime import date


class RecurrenceTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.h = Household.objects.create(name="Home")
        self.parent = U.objects.create_user("mumR", password="secret123", role="parent", household=self.h)
        self.child = U.objects.create_user("kidR", password="secret123", role="child", household=self.h)

    def _chore(self, recurrence, due):
        return Chore.objects.create(
            title="Trash", assignee=self.child, household=self.h,
            points=2, recurrence=recurrence, due_date=due, status="done")

    def test_daily_spawns_next_day(self):
        c = self._chore("daily", date(2026, 1, 10))
        nxt = c.spawn_next()
        self.assertEqual(nxt.due_date, date(2026, 1, 11))
        self.assertEqual(nxt.status, "assigned")
        self.assertEqual(nxt.recurrence, "daily")

    def test_weekly_spawns_same_weekday(self):
        c = self._chore("weekly", date(2026, 1, 10))
        nxt = c.spawn_next()
        self.assertEqual(nxt.due_date, date(2026, 1, 17))
        self.assertEqual(nxt.due_date.weekday(), c.due_date.weekday())

    def test_none_has_no_successor(self):
        c = self._chore("none", date(2026, 1, 10))
        self.assertIsNone(c.spawn_next())

    def test_verify_spawns_next_occurrence(self):
        c = self._chore("daily", date(2026, 1, 10))
        self.client.login(username="mumR", password="secret123")
        self.client.post(f"/chores/{c.id}/verify/")
        assigned = Chore.objects.filter(assignee=self.child, status="assigned", recurrence="daily")
        self.assertEqual(assigned.count(), 1)


class TallyTests(TestCase):
    def setUp(self):
        U = get_user_model()
        self.h = Household.objects.create(name="Home")
        self.parent = U.objects.create_user("mumT", password="secret123", role="parent", household=self.h)
        self.child = U.objects.create_user("kidT", password="secret123", role="child", household=self.h)
        Chore.objects.create(title="V", assignee=self.child, household=self.h, points=5, status="verified")
        Chore.objects.create(title="D", assignee=self.child, household=self.h, points=3, status="done")

    def test_tally_counts_only_verified(self):
        self.client.login(username="mumT", password="secret123")
        r = self.client.get("/tally/")
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, "5 pts")
        self.assertNotContains(r, "8 pts")

    def test_tally_updates_after_verification(self):
        c = Chore.objects.create(title="D2", assignee=self.child, household=self.h, points=4, status="done")
        self.client.login(username="mumT", password="secret123")
        self.client.post(f"/chores/{c.id}/verify/")
        r = self.client.get("/tally/")
        self.assertContains(r, "9 pts")
