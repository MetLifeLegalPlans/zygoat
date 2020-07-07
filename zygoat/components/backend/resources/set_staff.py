from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

"""
    A command for marking users as staff.

    ./manage.py set_staff --field email --users me@website.com you@website.com
    ./manage.py set_staff --int --users 1 2 5
"""


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--users", nargs="+", type=str, help="a list of user keys")
        parser.add_argument(
            "--field", type=str, default="pk", help="a unique field name on the user model"
        )
        parser.add_argument(
            "--int",
            action="store_true",
            help="the user keys should be interpreted as integers",
        )
        parser.add_argument(
            "--unset", action="store_true", help="set is_staff to False instead of True",
        )

    def handle(self, *args, **options):
        User = get_user_model()
        convert = int if options.get("int") else str
        user_values = [convert(v.strip()) for v in options.get("users")]
        where = {"{}__in".format(options.get("field")): user_values}
        users = User.objects.filter(**where)
        for u in users:
            u.is_staff = not options.get("unset")
        users = User.objects.bulk_update(users, ["is_staff"])
