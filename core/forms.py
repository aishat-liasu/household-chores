from django.contrib.auth.forms import UserCreationForm

from .models import User


class MemberCreationForm(UserCreationForm):
    """A parent uses this to create another family member's account."""

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "role")
