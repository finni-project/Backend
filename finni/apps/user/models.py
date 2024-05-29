from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import SoftDeletedMixin, TimeStampMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("The Email field must be set"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, SoftDeletedMixin, TimeStampMixin):
    email = models.EmailField(verbose_name=_("이메일"), unique=True)
    name = models.CharField(verbose_name=_("이름"), max_length=16)
    birth = models.DateField(verbose_name=_("생일"), null=True)
    is_active = models.BooleanField(verbose_name=_("활성화"), default=True)
    is_staff = models.BooleanField(verbose_name=_("관리자"), default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    class Meta:
        db_table = "user"

    def __str__(self):
        return self.email
