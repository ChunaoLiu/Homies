from django.db import models
from django.db import models
from django.db.models.deletion import CASCADE, SET, SET_NULL

# Create your models here.
class Dorm(models.Model):
    Dorm_id = models.AutoField(primary_key=True)
    capacity = models.IntegerField(null=False)
    gender = models.CharField(max_length=25)
    has_gym = models.BooleanField(default=False)
    has_study_room = models.BooleanField(default=False)
    has_game_room = models.BooleanField(default=False)
    num_ppl = models.IntegerField(null=False)
    max_ppl = models.IntegerField(null=False)

    class meta():
        db_table = 'Dorm'
        ordering = ['Dorm_id', 'num_ppl']

    def save(self, *args, **kwargs):
        super(Dorm, self).save(*args, **kwargs)
        self.num_ppl += 1

class Unit(models.Model):
    Unit_id = models.AutoField(primary_key=True)
    unit_name = models.CharField(max_length=25, default="Default")
    num_ppl = models.IntegerField()
    max_ppl = models.IntegerField()
    has_kitchen = models.BooleanField(default=False)
    has_laundry = models.BooleanField(default=False)
    Dorm_id = models.ForeignKey(to='API.Dorm', on_delete=models.SET_NULL, null=True)

    class meta():
        db_table = 'Unit'
        ordering = ['Unit_id', 'num_ppl']

    def save(self, *args, **kwargs):
        super(Unit, self).save(*args, **kwargs)
        self.num_ppl += 1


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, default="Bruh", unique=False)
    email = models.EmailField(default="No_EMAIL", unique=True)
    standing = models.CharField(max_length=25, unique=False)
    age = models.IntegerField(null=True, unique=False)
    gender = models.CharField(max_length=15, null=True, unique=False)
    RA_id = models.IntegerField(unique=True, null=True)
    Unit_id = models.ForeignKey(to=Unit, on_delete=models.SET_NULL, null=True)
    password = models.CharField(max_length = 25, default=12345)
    class meta():
        db_table = 'User'
        ordering = ['uid', 'name', 'email', 'RA_id', 'Unit_id']

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum RA_id value from the database
            last_id = User.objects.all().aggregate(largest=models.Max('RA_id'))['largest']

            # aggregate can return None! Check it first.
            # If it isn't none, just use the last ID specified (which should be the greatest) and add one to it
            if last_id is not None:
                self.RA_id = last_id + 1

        super(User, self).save(*args, **kwargs)


class Lease(models.Model):
    Lease_id = models.AutoField(primary_key=True)
    lease_type = models.CharField(max_length=25, default="Classic rippoff")
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(auto_now=True, null=True)
    User_id = models.OneToOneField(to=User, on_delete=models.CASCADE)
    Unit_id = models.ForeignKey(to='API.Unit', on_delete=models.SET_NULL, null=True)

    class meta():
        db_table = 'Lease'
        ordering = ['Lease_id', 'User_id', 'lease_type', 'start_date', 'end_date']

    def save(self, *args, **kwargs):
        if self._state.adding:
            last_unit = Lease.objects.all.aggregate(largest=models.Max('Unit_id'))['largest']
            if last_unit is not None:
                self.unit_id = last_unit + 1
        super (Lease, self).save(*args, **kwargs)



class Message(models.Model):
    msg_id = models.AutoField(primary_key=True)
    to = models.ForeignKey(to=User, related_name="recipient", on_delete=models.SET_NULL, null=True)
    fr = models.ForeignKey(to=User, related_name="sender", on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=256, default="Hi there!")

    class meta():
        db_table = 'Message'
        ordering = ['msg_id', 'to', 'fr', 'content']

    def save(self, *args, **kwargs):
        super (Message, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Event(models.Model):
    Event_id = models.AutoField(primary_key=True)
    Event_name = models.CharField(max_length=25)
    Description = models.CharField(max_length=50)
    Dorm_id = models.ForeignKey(to='API.Dorm', on_delete=models.SET_NULL, null=True)
    Date = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class EventRel(models.Model):
    uid = models.ForeignKey(to='API.User', on_delete=models.SET_NULL, null=True)
    Event_id = models.ForeignKey(to='API.Event', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class ResidentAssistant(models.Model):
    RA_id = models.AutoField(primary_key=True)
    RA_name = models.CharField(max_length = 40, unique=False)
    Title = models.CharField(max_length=20, default="Basic RA")
    Description = models.CharField(max_length=60, default="Basic RA duties: roam around the halls")

class WorkOrder(models.Model):
    Work_id = models.AutoField(primary_key=True)
    Submitter = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='Submitter', null=False)
    RA_assigned = models.ForeignKey(to=User, on_delete=models.DO_NOTHING, related_name='RA_assigned', null=True)
    Building_requested = models.ForeignKey(to=Unit, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length=255, null=True)
    Submit_time = models.DateField(auto_now=True)
    End_time = models.DateField(auto_now_add=True, null=True)
    status = models.BooleanField(default=False)

