from django.db import models


class CourseMaster(models.Model):
    course_code = models.CharField(max_length=100, unique=True)
    course_name = models.CharField(max_length=100)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.course_code} - {self.course_name}"

class StudentMaster(models.Model):
    # Many-to-Many relationship with CourseMaster
    courses = models.ManyToManyField(CourseMaster, blank=True, verbose_name="Courses")

    roll_number = models.CharField(max_length=20, blank=True, null=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=False)
    father_name = models.CharField(max_length=100, blank=True, null=True)
    shash = models.CharField(max_length=160, blank=True, null=True)
    createdon = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        courses_str = ", ".join([course.course_code for course in self.courses.all()])
        return f"{self.name} - Roll No: {self.roll_number} - Course: {courses_str} - Email: {self.email}"



class CertificatesMaster(models.Model):
    student = models.ForeignKey(StudentMaster, on_delete=models.CASCADE)
    certificate_name = models.CharField(max_length=200)
    certificate = models.FileField(upload_to='certificates/', blank=True, null=True)
    email_sent = models.BooleanField(default=False)
    chash       = models.CharField(max_length=160, blank=True, null=True)
    tid = models.CharField(max_length=160, blank=True, null=True)

    def __str__(self):
        return self.certificate_name