import csv
from django.http import HttpResponse
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CourseMaster, StudentMaster, CertificatesMaster
from django.utils.html import format_html
from .forms import CertificatesMasterAdminForm

# Add a method to get the course name for CertificatesMaster
def get_course_name(obj):
    return ", ".join([course.course_name for course in obj.student.courses.all()])
get_course_name.short_description = "Course Name"

# Define a custom method to get the courses and course codes as a comma-separated string
def get_courses_display(obj):
    courses = [f"{course.course_code} - {course.course_name}" for course in obj.courses.all()]
    return ", ".join(courses)

# Create a custom filter for courses
class CoursesFilter(admin.SimpleListFilter):
    title = 'Courses'
    parameter_name = 'courses'

    def lookups(self, request, model_admin):
        courses = CourseMaster.objects.all()
        return [(course.course_code, course.course_name) for course in courses]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(courses__course_code=self.value())
        return queryset



# Custom method to display certificates as links
def get_certificates_display(obj):
    certificates = obj.certificatesmaster_set.all()
    if certificates:
        links = []
        for certificate in certificates:
            links.append(
                format_html('<a href="{}">{}</a>', certificate.certificate.url, certificate.certificate_name)
            )
        return format_html('<br>'.join(links))
    else:
        return "No certificates available"
get_certificates_display.short_description = "Certificates"


# Custom admin action to export selected students to CSV
def export_students_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write the CSV header row
    header = ['Name', "Father's Name", 'Email', 'Roll Number', 'Courses Enrolled', 'Certificates']
    writer.writerow(header)

    # Write student data to CSV
    for student in queryset:
        courses = get_courses_display(student)
        certificates = get_certificates_display(student)
        writer.writerow([student.name, student.father_name, student.email, student.roll_number, courses, certificates])

    return response

export_students_to_csv.short_description = "Export selected students to CSV"

# Create a custom admin class for User
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'last_login', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register the CourseMaster model
@admin.register(CourseMaster)
class CourseMasterAdmin(admin.ModelAdmin):
    list_display = ('course_code', 'course_name', 'start_date', 'end_date')
    list_filter = ('course_code', 'course_name', 'start_date', 'end_date')
    search_fields = ['course_code', 'course_name']

# Register the StudentMaster model
@admin.register(StudentMaster)
class StudentMasterAdmin(admin.ModelAdmin):
    list_display = (get_courses_display, get_certificates_display, 'roll_number', 'name', 'father_name', 'email', 'shash')
    list_filter = (CoursesFilter,)
    search_fields = ['name', 'email', 'roll_number']
    actions = [export_students_to_csv]

    def get_courses_display(self, obj):
        return ", ".join([course.course_name for course in obj.courses.all()])
    get_courses_display.short_description = "Courses"

# Register the CertificatesMaster model
@admin.register(CertificatesMaster)
class CertificatesMasterAdmin(admin.ModelAdmin):
    form = CertificatesMasterAdminForm  # Use the custom form for adding/editing
    list_display = ('student', 'certificate_name', 'email_sent', 'chash', 'tid')  # Include chash and tid in list_display
    list_filter = ('student__courses', 'email_sent')
    search_fields = ['student__name', 'student__email', 'certificate_name']

    def get_list_display(self, request):
        # Override get_list_display to include chash and tid conditionally
        if 'action' in request.GET:
            # When performing bulk actions, exclude chash and tid
            return ('student', 'certificate_name')
        return self.list_display

# Unregister the default User admin and register the custom User admin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)