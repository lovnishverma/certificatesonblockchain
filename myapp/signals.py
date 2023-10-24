from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.core.mail import send_mail
from django.utils import timezone
from .models import StudentMaster
from .models import CertificatesMaster

@receiver(pre_save, sender=StudentMaster)
def add_createdon(sender, instance, **kwargs):
    if not instance.createdon:
        instance.createdon = timezone.now()

# Define the function to generate the student hash
def generate_student_shash(name, father_name, roll_number):
    current_time = datetime.now()
    # Generate the hash using the student's information
    student_shash = hash((name, father_name, roll_number, current_time))
    return student_shash

# Signal receiver to add the hash when a new student is saved
@receiver(post_save, sender=StudentMaster)
def add_student_shash(sender, instance, created, **kwargs):
    if created:  # Only generate the hash for new students
        instance.shash = generate_student_shash(instance.name, instance.father_name, instance.roll_number)
        instance.save()

# Define the function to generate the CERTIFICATE hash
def generate_student_chash(student, certificate_name, certificate):
    current_time = datetime.now()
    # Generate the hash using the student's information
    student_chash = hash((student, certificate_name, certificate, current_time))
    return student_chash

# Signal receiver to add the hash when a new CERTIFICATE is saved
@receiver(post_save, sender=CertificatesMaster)
def add_student_chash(sender, instance, created, **kwargs):
    if created:  # Only generate the hash for new students
        instance.chash = generate_student_chash(instance.student, instance.certificate_name, instance.certificate)
        instance.save()

@receiver(pre_save, sender=CertificatesMaster)
def send_email_notification(sender, instance, **kwargs):
    # Check if the email field has been updated
    if instance.pk:  # If the instance has a primary key, it's an update
        original_instance = CertificatesMaster.objects.get(pk=instance.pk)
        if instance.student.email != original_instance.student.email:
            # Email field has been updated, send email notification
            student_name = original_instance.student.name
            certificate_name = instance.certificate_name
            subject = f' Hey! "{student_name}" Your certificate "{certificate_name}" has been updated'
            message = f'Your certificate "{certificate_name}" has been updated at https://nielitcertificates.pythonanywhere.com Register with your email to download Certificate if already registered Login and download your Certificate'
            from_email = 'nielitcertificates@gmail.com'
            recipient_email = original_instance.student.email

            send_mail(subject, message, from_email, [recipient_email])

    # For new certificates (created)
    elif not instance.email_sent:
        student_name = instance.student.name  # Use instance for new certificates
        certificate_name = instance.certificate_name
        subject = f' Hey! "{student_name}" Your certificate "{certificate_name}" has been updated'
        message = f'Your certificate "{certificate_name}" has been updated at https://nielitcertificates.pythonanywhere.com Register with your email to download Certificate if already registered Login and download your Certificate'
        from_email = 'nielitcertificates@gmail.com'
        recipient_email = instance.student.email  # Use instance for new certificates

        send_mail(subject, message, from_email, [recipient_email])

        # Update the email_sent field to prevent sending duplicate emails
        instance.email_sent = True
