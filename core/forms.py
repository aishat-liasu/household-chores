from django.contrib.auth.forms import UserCreationForm

from .models import User


class MemberCreationForm(UserCreationForm):
    """A parent uses this to create another family member's account."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "role")


from django import forms

from .models import Chore


class ChoreForm(forms.ModelForm):
    """Parent-facing form to create and assign a chore within their household."""

    class Meta:
        model = Chore
        fields = ("title", "description", "points", "assignee", "recurrence")

    def __init__(self, *args, household=None, **kwargs):
        super().__init__(*args, **kwargs)
        if household is not None:
            self.fields["assignee"].queryset = household.members.all()
        else:
            self.fields["assignee"].queryset = User.objects.none()
