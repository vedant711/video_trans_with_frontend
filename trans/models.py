from django.db import models

# Create your models here.
class Logs(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50)
    start_datetime = models.CharField(max_length=150)
    path = models.CharField(max_length=150)
    source = models.CharField(max_length=1000)
    callback_url = models.CharField(max_length=2000)
    queueId = models.CharField(max_length=2000)
    user = models.CharField(max_length=200)

    class Meta:
        managed = True
        db_table = 'logs'