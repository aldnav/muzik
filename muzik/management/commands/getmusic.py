from django.core.management.base import BaseCommand, CommandError
from muzik.utils import get_music


class Command(BaseCommand):
    help = 'Gets music from various sources'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_id', nargs='+', type=int)

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Fetching music...'))
        get_music()
        self.stdout.write(self.style.SUCCESS('Fetching music successful!'))
