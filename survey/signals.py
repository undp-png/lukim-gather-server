from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from region.models import ProtectedArea, Region

from .models import HappeningSurvey


@receiver(post_save, sender=HappeningSurvey)
def send_survey_approval_notification(sender, instance, created, **kwargs):
    update_fields = kwargs.get("update_fields")
    if update_fields and "is_public" in update_fields:
        if instance.is_public == False:
            if instance.updated_by:
                instance.created_by.notify(
                    instance.updated_by,
                    f'has made the project "{instance.title}" private',
                    action_object=instance,
                    notification_type=f"happening_survey_private",
                )
                instance.created_by.send_push_notification(
                    message=f"{instance.updated_by} has made the project '{instance.title}' private."
                )
                return
    if update_fields and "status" in update_fields:
        if instance.status == "pending":
            return
        if instance.created_by:
            instance.created_by.notify(
                instance.updated_by,
                instance.status,
                action_object=instance,
                notification_type=f"happening_survey_{instance.status}",
                description=f'Admin has {instance.status} the project "{instance.title}".',
            )
            instance.created_by.send_push_notification(
                message=f'Admin has {instance.status} the project "{instance.title}".'
            )
            return
    if created or (
        update_fields
        and any(field in update_fields for field in ["boundary", "location"])
    ):
        region_geo = instance.location if instance.location else instance.boundary
        survey_region = (
            Region.objects.filter(boundary__bbcontains=region_geo).first()
            if region_geo
            else None
        )
        protected_area = (
            ProtectedArea.objects.filter(boundary__bbcontains=region_geo).first()
            if region_geo
            else None
        )
        instance.region = survey_region
        instance.protected_area = protected_area
        instance.save()
