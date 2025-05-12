from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile
from two_factor.plugins.phonenumber.models import PhoneDevice


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()



@receiver(user_logged_in)
def create_profile_on_login(sender, request, user, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)

    if profile.phone_number:
        phone_number = profile.phone_number.as_e164
        device, created = PhoneDevice.objects.get_or_create(
            user=user,
            defaults={'number': phone_number, 'confirmed': True}
        )
        if not created and device.number != phone_number:
            device.number = phone_number
            device.save()

@receiver(post_save, sender=UserProfile)
def create_or_update_phone_device(sender, instance, **kwargs):
    phone_number = instance.phone_number
    if phone_number:
        phone_number_e164 = phone_number.as_e164
        device_qs = PhoneDevice.objects.filter(user=instance.user)
        if device_qs.exists():
            device = device_qs.first()
            if device.number != phone_number_e164:
                device.number = phone_number_e164
                device.save()
        else:
            PhoneDevice.objects.create(
                user=instance.user,
                number=phone_number_e164,
                confirmed=True
            )