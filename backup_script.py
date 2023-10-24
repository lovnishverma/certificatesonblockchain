import os

# Determine the path to your Django project's manage.py file
manage_py_path = '/home/nielitcertificates/myapp/manage.py'

# Run the dumpdata management command using manage.py
os.system(f"python {manage_py_path} dumpdata > /home/nielitcertificates/myapp/daily_database_backup.json")