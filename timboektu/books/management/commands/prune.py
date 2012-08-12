from django.core.management.base import BaseCommand, CommandError
from timboektu.books.models import Post
import datetime
from datetime import date, timedelta
from django.core.mail import send_mail
from timboektu.books.config import *
from django.template.loader import render_to_string

class Command(BaseCommand):

    def handle(self, *args, **options):
        # Remove old posts
        self.remove_old_posts()
        # Send notices to aging posts
        self.notify_aging_posts()
        
    def notify_aging_posts(self):
        # Find all aging posts
        notify_date = datetime.datetime.now() - timedelta(days = NOTIFY_THRESHOLD)
        posts = Post.objects.filter(mdate__lte=notify_date).filter(notified=False)
        
        self.stdout.write('Will notify: ')
        for p in posts:
           self.stdout.write('%s, ' % p.id)
        if CRON_DEBUG:
            self.stdout.write(' (abort) ')
            return
        
        # Send warning emails to old post owners with a renewal link
        for p in posts:
            send_mail(
                  'TimBoekTU: Renewal request for ' + p.title,
                   render_to_string('emails/renew.html', 
                                    {
                                     'post' : p,
                                     'notify' : NOTIFY_THRESHOLD,
                                     'delete' : DELETE_THRESHOLD,
                                     'delta' : DELETE_THRESHOLD - NOTIFY_THRESHOLD
                                    }), 
                   'services@timboektu.com',
                   [p.email], 
                   fail_silently=True)
            p.notified = True;
            # Save but don't update modify date
            p.save(skip_mdate=True)
        
    def remove_old_posts(self):
        # Remove old posts
        delete_date = datetime.datetime.now() - timedelta(days = DELETE_THRESHOLD)
        posts = Post.objects.filter(mdate__lte=delete_date)
        
        self.stdout.write('Will delete: ')
        for p in posts:
           self.stdout.write('%s, ' % p.id)
        if CRON_DEBUG:
            self.stdout.write(' (abort) ')
            return
        
        posts.delete()
