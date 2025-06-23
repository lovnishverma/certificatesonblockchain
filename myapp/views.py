from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import StudentMaster, CertificatesMaster
from .forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages
import qrcode
from io import BytesIO
from base64 import b64encode


@login_required
def home(request):
    if request.user.username == 'admin':
        certificates = CertificatesMaster.objects.all().order_by('-id')
        return render(request, 'admin.html', {'certificates': certificates})
    else:
        students = StudentMaster.objects.filter(email=request.user.email)

        # Create a dictionary to store student data and associated QR code URLs
        student_data = []

        for student in students:
            student_certificates = student.certificatesmaster_set.all()

            # Generate QR code URLs for each certificate
            qr_code_urls = []

            for certificate in student_certificates:
                # Build the certificate URL using request.build_absolute_uri
                certificate_url = request.build_absolute_uri(
                    certificate.certificate.url)

                # Create a QR code for the certificate URL
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=10,
                    border=4,
                )
                qr.add_data(certificate_url)
                qr.make(fit=True)

                # Create an in-memory binary stream to store the image
                stream = BytesIO()
                qr.make_image(fill_color="black", back_color="white").save(
                    stream, format="PNG")

                # Encode the binary image data as base64
                image_base64 = b64encode(stream.getvalue()).decode("utf-8")

                # Create a data URL for the image
                data_url = f"data:image/png;base64,{image_base64}"

                qr_code_urls.append(data_url)

            student_data.append({
                'student': student,
                'certificates': student_certificates,
                'qr_code_urls': qr_code_urls,
            })

        return render(request, 'home.html', {'students': students, 'students_data': student_data})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check if the email already exists
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, 'This email address is already registered. If you forgot your username or password, please reset your password. You will receive a link to reset your password in your email along with your username.')
            else:
                # If the email is unique, save the user
                form.save()
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': form})


def privacy_policy(request):
    # You can add any context data you want to pass to the template here
    context = {
        'title': 'Privacy Policy',
        'content': 'This is your Privacy Policy content.',
        # Add more data as needed
    }

    # Render the Privacy Policy template with the context data
    return render(request, 'privacy_policy.html', context)


def save_transaction(request, certificate_id, transaction_hash):
    try:
        # Find the certificate by its ID
        certificate = CertificatesMaster.objects.get(id=certificate_id)

        # Save the transaction hash to the certificate
        certificate.tid = transaction_hash
        certificate.save()

        # Pass the transaction hash to the success page
        return render(request, 'success.html', {'transaction_hash': transaction_hash})

    except CertificatesMaster.DoesNotExist:
        # Handle the case where the certificate is not found
        return render(request, 'certificate_not_found.html')

    except Exception as e:
        # Handle other exceptions
        return render(request, 'error.html', {'error_message': str(e)})
