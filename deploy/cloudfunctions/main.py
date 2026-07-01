# fitness-tracker/deploy/cloudfunctions/main.py
import functions_framework
from scheduler import run_daily_sync

@functions_framework.http
def main(request):
    run_daily_sync()
    return "OK", 200
