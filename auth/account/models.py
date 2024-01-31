from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser

#  Custom User Manager
# AbstractBaseUser is a class provided by Django that you can use to create a custom user model in your Django project. It's part of the Django authentication system and is designed to be a base class for creating user models with custom fields and behavior.
# ye baseusermanager ko inherit karke bana hua hai 
#  BaseUserManager is a Django base class for creating custom manager classes for user models. It's used in conjunction with custom user models and provides a set of methods for creating and managing user instances. This class is often subclassed to create a manager tailored for your specific user model. 
class UserManager(BaseUserManager):
  def create_user(self, email, name, tc, password=None, password2=None):
      """
      Creates and saves a User with the given email, name, tc and password.
      """
      if not email:
          raise ValueError('User must have an email address')

      user = self.model(
          email=self.normalize_email(email),
          name=name,
          tc=tc,
      )
     # because of this pwd will be saved with hased 
      user.set_password(password)
      user.save(using=self._db)
      return user

  def create_superuser(self, email, name, tc, password=None):
      """
      Creates and saves a superuser with the given email, name, tc and password.
      """
      user = self.create_user(
          email,
          password=password,
          name=name,
          tc=tc,
      )
      user.is_admin = True
      user.save(using=self._db)
      return user

#  Custom User Model
class User(AbstractBaseUser):
  email = models.EmailField(
      verbose_name='Email',
      max_length=255,
      unique=True,
  )
  name = models.CharField(max_length=200)
  tc = models.BooleanField()
  is_active = models.BooleanField(default=True)
  is_admin = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  objects = UserManager()

#  this means user name se login nahi bilki email se login hoga , and baki required feilds hoge 
   
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['name', 'tc']
#  jab bhi hum object ko dikhayege to email ke through dikhayege 
  
  def __str__(self):
      return self.email

  def has_perm(self, perm, obj=None):
      "Does the user have a specific permission?"
      # Simplest possible answer: Yes, always
      return self.is_admin

  def has_module_perms(self, app_label):
      "Does the user have permissions to view the app `app_label`?"
      # Simplest possible answer: Yes, always
      return True

  @property
  def is_staff(self):
      "Is the user a member of staff?"
      # Simplest possible answer: All admins are staff
      return self.is_admin