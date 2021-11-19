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
        super(Dorm, self).save(*args, **kwargs)
        self.num_ppl += 1


class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25, default="Bruh")
    email = models.EmailField(default="No_EMAIL")
    standing = models.CharField(max_length=25)
    age = models.IntegerField(null=False)
    gender = models.CharField(max_length=15, null=False)
    RA_id = models.IntegerField(unique=True, null=True)
    Unit_id = models.ForeignKey(to='API.Unit', on_delete=models.SET_NULL, null=True)
    class meta():
        db_table = 'User'
        ordering = ['uid', 'name', 'email', 'RA_id', 'Unit_id']

    def save(self, *args, **kwargs):
        # This means that the model isn't saved to the database yet
        if self._state.adding:
            # Get the maximum RA_id value from the database
            last_id = self.objects.all().aggregate(largest=models.Max('RA_id'))['largest']

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

    def __str__(self):
        return self.name
