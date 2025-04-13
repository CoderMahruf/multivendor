from apps.accounts.utils import send_notification
from django.db import models
from apps.accounts.models import User,UserProfile
# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,related_name='user_profile',on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_slug = models.SlugField(max_length=100,unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.vendor_name 
    
    def save(self,*args,**kwargs):
        if self.pk is not None:
            # Update
            orig = Vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context={
                    'user':self.user,
                    'is_approved':self.is_approved,
                    'to_email':self.user.email
                }
                if self.is_approved == True:
                    # send notification email 
                    mail_subject = 'Congratulations! Your restaurent has been approved.'
                    send_notification(mail_subject,mail_template,context)
                else:
                    # send notification email 
                    mail_subject = 'We are sorry! You are not eligible for publishing your food meny on our marketplace.'
                    send_notification(mail_subject,mail_template,context)
        return super(Vendor,self).save(*args,**kwargs)
        