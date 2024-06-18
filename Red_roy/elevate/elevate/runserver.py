import subprocess
from django.core.management.base import BaseCommand

help = 'Run the server and Tailwind in parallel'

def handle():
        # Start the Django server
        server = subprocess.Popen(['python3', 'manage.py', 'runserver','0.0.0.0:8000'])
        
        # Start Tailwind
        tailwind = subprocess.Popen(['python3', 'manage.py', 'tailwind', 'start'])

        # Wait for both processes to complete
        try:
            server.wait()
            tailwind.wait()
        except KeyboardInterrupt:
            server.terminate()
            tailwind.terminate()
            server.wait()
            tailwind.wait()
   
handle()