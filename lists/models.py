from django.db import models

## to clear db:
## rm db.sqlite3
## python manage.py migrate --noinput
	
class List (models.Model):
	pass
	
class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, default=None)
