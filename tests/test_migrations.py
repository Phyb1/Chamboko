import pytest
from django.core.management import call_command


def test_models_and_migrations_are_in_sync(db):
    try:
        call_command("makemigrations", "--check", "--dry-run", verbosity=0)
    except SystemExit:
        pytest.fail("The models changed without a migration. Run: python manage.py makemigrations core")
