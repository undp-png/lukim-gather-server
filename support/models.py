from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from lukimgather.models import TimeStampedModel, UserStampedModel


class LegalDocumentTypeChoice(models.TextChoices):
    TERMS_AND_CONDITIONS = "terms-and-conditions", _("Terms And Conditions")
    PRIVACY_POLICY = "privacy-policy", _("Privacy Policy")
    COOKIE_POLICY = "cookie-policy", _("Cookie Policy")


class LegalDocument(UserStampedModel, TimeStampedModel):
    document_type = models.CharField(
        _("document type"),
        max_length=20,
        choices=LegalDocumentTypeChoice.choices,
        unique=True,
    )
    description = RichTextField(_("description"))

    def __str__(self):
        return self.document_type

    def save(self, *args, **kwargs):
        if self.pk:
            cls = self.__class__
            old = cls.objects.get(pk=self.pk)
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    old_val = getattr(old, field_name)
                    new_val = getattr(self, field_name)
                    if hasattr(field, "is_custom_lower_field"):
                        if field.is_custom_lower_field():
                            new_val = new_val.lower()
                    if old_val != new_val:
                        changed_fields.append(field_name)
                except Exception:
                    pass
            kwargs["update_fields"] = changed_fields
        super().save(*args, **kwargs)


class Feedback(UserStampedModel, TimeStampedModel):
    title = models.CharField(_("title"), max_length=255)
    description = RichTextField(_("description"))

    def __str__(self):
        return self.title