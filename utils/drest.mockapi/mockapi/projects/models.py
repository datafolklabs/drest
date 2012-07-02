
from django.db import models

class Project(models.Model):
    class Meta:
        db_table = 'projects'
        
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True, auto_now=True)                     
    label = models.CharField(max_length=128, blank=False, unique=True)
    
    def __unicode__(self):
        return unicode(self.label)
    
    def __str__(self):
        return self.label