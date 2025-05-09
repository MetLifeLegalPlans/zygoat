"""
Checks every half second to see if your database can be connected to successfully.

Once a connection is made, the command returns 0. If a connection can never be made,
it blocks indefinitely.
"""

from time import sleep
from typing import Any

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    def handle(self, *args: Any, **kwargs: Any) -> None:
        while True:
            sleep(0.5)
            try:
                with connection.temporary_connection():
                    self.stdout.write(self.style.SUCCESS("Connected to db."))
                    break
            except OperationalError:
                self.stdout.write(self.style.WARNING("Still waiting for db..."))
