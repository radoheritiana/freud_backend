from django.db import models
from helpers.models import TrackingModel
from django.contrib.auth.models import (PermissionsMixin, AbstractBaseUser, UserManager)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.apps import apps
from django.contrib.auth.hashers import make_password
import jwt
from datetime import datetime, timedelta
from django.conf import settings


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TrackingModel):
    username = None
    first_name = models.CharField(_("first name"), max_length=255, blank=True)
    last_name = models.CharField(_("last name"), max_length=255, blank=True)
    email = models.EmailField(_("email address"), blank=False, unique=True)
    gender = models.CharField(_("gender"), max_length=10, blank=True, null=True)
    age = models.IntegerField(_("age"), blank=True, null=True)
    weight = models.FloatField(_("Weight"), blank=False, null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    """email_verified = models.BooleanField(
        _("email_verified"),
        default=False,
        help_text=_(
            "Designates whether this user email is verified. "
        ),
    )"""    
    
    objects = CustomUserManager()
    
    @property
    def token(self):
        token = jwt.encode({'email': self.email, 'exp': datetime.utcnow() + timedelta(hours=24)}, settings.SECRET_KEY, algorithm='HS256')
        return token

