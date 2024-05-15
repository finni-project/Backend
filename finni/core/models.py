from django.db import models


class SoftDeleteQuerySet(models.QuerySet):
    def delete(self):
        self.update(is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeletedMixin(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = SoftDeleteManager.from_queryset(SoftDeleteQuerySet)()

    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.save(update_fields=["is_deleted"])

    class Meta:
        abstract = True


class TimeStampMixin(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
