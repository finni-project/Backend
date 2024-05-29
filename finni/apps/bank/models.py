from django.core.validators import MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from apps.user.models import User
from core.models import SoftDeletedMixin, TimeStampMixin


class Allowance(SoftDeletedMixin, TimeStampMixin):
    user = models.OneToOneField(
        User, verbose_name="회원", on_delete=models.DO_NOTHING
    )
    cycle = models.IntegerField(
        verbose_name="용돈 주기", validators=[MinValueValidator(1)]
    )
    amount = models.IntegerField(
        verbose_name="용돈 금액", validators=[MinValueValidator(1)]
    )

    class Meta:
        db_table = "allowance"
        verbose_name = "용돈 정보"
        verbose_name_plural = "용돈 정보 목록"


class AllowanceCategory(SoftDeletedMixin, TimeStampMixin):
    allowance = models.ForeignKey(
        Allowance, verbose_name="용돈 정보", on_delete=models.DO_NOTHING, related_name='allowance_categories'
    )
    name = models.CharField(verbose_name="용돈 분류", max_length=6)
    icon = models.CharField(verbose_name="용돈 분류 아이콘", max_length=16)

    class Meta:
        db_table = "allowance_category"
        verbose_name = "용돈 분류"
        verbose_name_plural = "용돈 분류 목록"

    def save(self, *args, **kwargs):
        if self.allowance.allowance_categories.count() >= 15:
            raise ValidationError("An instance of Allowance can only have up to 15 instances of AllowanceCategory.")

        super().save(*args, **kwargs)
