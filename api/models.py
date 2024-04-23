from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        self.save(user)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        self.save(self.model)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has a permission.
        """
        return self.is_staff

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions for the given app label.
        """
        return self.is_staff

class MCU(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Foreign key to User model
    waterPumpVal = models.BooleanField(default=False)

    def __str__(self):
        return f"Water Pump State for User {self.user.email}: {'On' if self.waterPumpVal else 'Off'}"    
    
class SensorData(models.Model):
    
    # Foreign key to User model (who took has the access)
    mcuId = models.ForeignKey(MCU, on_delete=models.SET_NULL, null=True, default=None)

    # sensorDataID = models.IntegerField(primary_key=True)
    # sensorDataID = models.AutoField(primary_key=True)  # Auto-incrementing primary key

    soilMoisture = models.IntegerField()
    temperature = models.IntegerField()
    humidity = models.IntegerField()
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f" (soilMoisture: {self.soilMoisture}, temperature: {self.temperature}, humidity: {self.humidity} at {self.dateTime}) from: {self.mcuId}"

class Action(models.Model):
    # Foreign key to User model (who took the action)
    # Foreign key to SensorData model (action is related to specific sensor data)
    sensorData = models.ForeignKey(SensorData, on_delete=models.CASCADE)
    waterPumpVal = models.BooleanField()


    def __str__(self):
        return f"water pump ({self.waterPumpVal}) for sensor data (soilMoisture: {self.sensorData.soilMoisture}, temperature: {self.sensorData.temperature}, humidity: {self.sensorData.humidity} at {self.sensorData.dateTime})"
    
