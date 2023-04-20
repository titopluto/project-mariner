import uuid

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from permission.models import Permission

alphanumeric = RegexValidator(
    r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed."
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        if not email:
            raise ValueError("The given email must be set")
        if not username:
            raise ValueError("The given username must be set")
        if not password:
            raise ValueError("A password must be set")

        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, username, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, username, password, **extra_fields)

    def create_superuser(
        self, email=None, username=None, password=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, username, password, **extra_fields)

    def update_password(self, password, email=None, username=None):
        if email is None and username is None:
            raise ValueError("User must supply either an email or username")
        if email:
            try:
                user = self.model.objects.get(email=email)
                user.set_password(password)
                user.save(using=self._db)
                return user
            except:
                raise ValueError("User does not exist")

        else:
            try:
                user = self.model.objects.get(username=username)
                user.set_password(password)
                user.save(using=self._db)
                return user
            except:
                raise ValueError("User does not exist")


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    permissions = models.ManyToManyField("permission.Permission", related_name="users")
    email = models.EmailField(_("email address"), max_length=255, unique=True)
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        blank=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[alphanumeric],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    given_name = models.CharField(
        _("Given name"), max_length=30, blank=False, null=False
    )
    family_name = models.CharField(
        _("Family name"), max_length=30, blank=False, null=False
    )
    birthdate = models.DateField(_("Birthdate"), blank=True, null=True)

    gender = models.CharField(_("sex"), max_length=10, blank=True)
    phone_number = models.CharField(_("phone number"), max_length=15, blank=True)
    date_joined = models.DateTimeField(
        _("date joined"), auto_now=False, auto_now_add=True
    )
    date_updated = models.DateTimeField(_("last update"), auto_now=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user is \
                                    a department staff"
        ),
    )
    is_admin = models.BooleanField(
        _("admin status"),
        default=False,
        help_text=_(
            "Designates whether the user \
                                    can log into this admin site."
        ),
    )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates whether the user \
                                        is a superuser"
        ),
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    @property
    def full_name(self):
        """
        Return the give_name plus the first_name, with a space in between.
        """
        full_name = "%s %s" % (self.given_name, self.family_name)
        return full_name.strip()

    def grant_permission(self, permission_id):
        permission = Permission.objects.get(id=permission_id)
        if permission:
            return self.permissions.add(permission)

    def revoke_permission(self, permission_id):
        permission = Permission.objects.get(id=permission_id)
        if permission:
            return self.permissions.remove(permission)
