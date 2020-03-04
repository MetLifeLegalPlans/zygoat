from time import sleep

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        while True:
            sleep(0.5)
            try:
                with connection.temporary_connection():
                    self.stdout.write(self.style.SUCCESS("Connected to db."))
                    break
            except OperationalError:
                self.stdout.write(self.style.WARNING("Still waiting for db..."))
