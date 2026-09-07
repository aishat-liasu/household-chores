from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import Chore, Household


class Command(BaseCommand):
    help = "Create a demo household with members and chores (idempotent; dev only)."

    def handle(self, *args, **options):
        User = get_user_model()

        # Idempotent reset: remove any previous demo data first.
        Household.objects.filter(name="Demo Household").delete()
        User.objects.filter(username__startswith="demo_").delete()

        hh = Household.objects.create(name="Demo Household")
        parent = User.objects.create_user("demo_parent", password="demo12345", role="parent", household=hh)
        User.objects.create_user("demo_parent2", password="demo12345", role="parent", household=hh)
        child = User.objects.create_user("demo_child", password="demo12345", role="child", household=hh)
        child2 = User.objects.create_user("demo_child2", password="demo12345", role="child", household=hh)

        Chore.objects.create(title="Set the table", assignee=child, household=hh, points=2, status="assigned")
        Chore.objects.create(title="Take out the bins", assignee=child2, household=hh, points=3, status="done")
        Chore.objects.create(title="Tidy your room", assignee=child, household=hh, points=5, status="verified")
        Chore.objects.create(title="Feed the dog", assignee=child, household=hh, points=1,
                             recurrence="daily", status="assigned", due_date=date.today())
        Chore.objects.create(title="Wash the car", assignee=child2, household=hh, points=8,
                             recurrence="weekly", status="assigned", due_date=date.today())

        self.stdout.write(self.style.SUCCESS(
            "Seeded 'Demo Household': 4 members, 5 chores. "
            "Dev logins: demo_parent / demo_child (password demo12345)."))
