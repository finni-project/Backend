from django.db import models

from apps.user.models import User
from core.models import SoftDeletedMixin, TimeStampMixin


class Allowance(SoftDeletedMixin, TimeStampMixin):
    user = models.OneToOneField(
        User, verbose_name="검토 요청자", on_delete=models.DO_NOTHING
    )
    cycle = models.IntegerField(verbose_name="용돈 주기")
    amount = models.IntegerField(verbose_name="용돈 금액")
    category = models.CharField(verbose_name="용돈 분류", max_length=6)

    class Meta:
        db_table = "review_request"
        verbose_name = "용돈 정보"
        verbose_name_plural = "용돈 정보 목록"


class Saving(SoftDeletedMixin, TimeStampMixin):
    ...


class SavingHistory(SoftDeletedMixin, TimeStampMixin):
    ...
