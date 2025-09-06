from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from tasks.models import Task, Category, Priority, Note, SubTask

class Command(BaseCommand):
    help = 'Populates the database with fake data'
    
    def handle(self, *args, **options):
        fake = Faker()
        
        all_priorities = list(Priority.objects.all())
        all_categories = list(Category.objects.all())
        
        if not all_priorities:
            self.stdout.write(self.style.ERROR('No priorities found. Please add them manually first.'))
            return
            
        if not all_categories:
            self.stdout.write(self.style.ERROR('No categories found. Please add them manually first.'))
            return
        
        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=fake.random_element(elements=all_priorities),
                category=fake.random_element(elements=all_categories)
            )
            
            for _ in range(fake.random_int(min=0, max=5)):
                SubTask.objects.create(
                    task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
                )
            
            for _ in range(fake.random_int(min=0, max=3)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2)
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 20 tasks'))