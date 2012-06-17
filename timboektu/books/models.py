from django.db import models
from django.forms import ModelForm
from django.db.models.query import QuerySet

class QuerySetManager(models.Manager):
    
    def get_query_set(self):
        return self.model.QuerySet(self.model)
    def __getattr__(self, attr, *args):
        return getattr(self.get_query_set(), attr, *args)
 
class Department(models.Model):
    title = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['title']
        
    def __unicode__(self):
        return self.title
    
class Post(models.Model):
    objects = QuerySetManager()
    
    class QuerySet(QuerySet):
        
        # Words to filter out
        stop_list = ['a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 
                 'from', 'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on',
                 'that', 'the', 'to', 'was', 'were', 'will', 'with']
        
        # Extend order_by to be case insensitive for title field
        def order_by(self, *field_names):
            if 'title' in field_names:
                field_list = [field.replace('title','lower_title') for field in field_names]
                self = self.extra(select={'lower_title': 'lower(title)'})
                return QuerySet.order_by(self, *field_list)
            
            return QuerySet.order_by(self, *field_names)
        
        def query_filter(self, query):
            from django.db.models import Q
            import operator
            import re
            
            strings = []
            
            # Add quoted strings
            quoted = re.findall('".+?"', query)
            for s in quoted:
                strings.append(re.sub('"','',s))
            
            # Add unquoted terms
            unquoted = re.sub('".+?"', '', query)
            for s in unquoted.split(','):
                if s:
                    strings += s.split(' ')
            
            # Remove common strings
            strings = filter(lambda s: s not in self.stop_list, strings)
            
            # Build and execute query
            posts = self.none()
            if strings:
                ors = []
                for s in strings:
                    ors.append(Q(title__icontains=s))
                    ors.append(Q(description__icontains=s))
                    ors.append(Q(authors__icontains=s))
                    ors.append(Q(courses__icontains=s))
                    ors.append(Q(isbn__icontains=s))
               
                posts = self.filter(reduce(operator.or_, ors))
        
            return posts
        
    
    
    title = models.CharField("Book title", max_length=1000)
    authors = models.CharField(blank=True, max_length=1000)
    EDITION_CHOICES = (
        ('1', '1st'),
        ('2', '2nd'),
        ('3', '3rd'),
        ('4', '4th'),
        ('5', '5th'),
        ('6', '6th'),
        ('7', '7th'),
        ('8', '8th'),
        ('9', '9th'),
    )
    edition = models.CharField(max_length=2, choices=EDITION_CHOICES, blank=True)
    year = models.CharField("Year of publication", max_length=4, blank=True)
    isbn = models.CharField("ISBN", max_length=13, blank=True) # http://djangosnippets.org/snippets/1994/
    courses = models.TextField("Relevant courses", blank=True)
    description = models.TextField(blank=True,
                                   help_text='For example: Dutch language book, good condition.')
    departments = models.ManyToManyField(Department)
    #photo = models.ImageField(blank=True)
    crdate = models.DateTimeField(auto_now=True)
    mdate = models.DateTimeField(auto_now=True)
    hash = models.CharField(max_length=100, editable=False, blank=True)
    
    name = models.CharField("Your first name", max_length=100)
    email = models.EmailField("Your email")
    price = models.DecimalField("Asking price", max_digits=5, decimal_places=2, null=True, blank=True,
                                help_text='Defaults to "Best Offer" when left blank')
    
    class Meta:
        ordering = ['-crdate']
    
    def __unicode__(self):
        return self.title
    
class PostForm(ModelForm):
    class Meta:
        model = Post
