from django.conf import settings
from django.db import models
from django.dispatch import receiver
import os
from django.utils import timezone
from .validator import validate_file_extension
from django.utils.translation import ugettext_lazy as _

def embed_image(text,images):
    text = str(text)
    for image in images:
        old = '[{0}]'.format(image.title)
        new = '<img src="/static/media/{name} class="img-responsive img-circle margin" style="display:inline" alt="Bird" width="{width}" height="{height}">'.format(name =image.title,width=image.width,height=image.height)
        text = text.replace(old,new)
    return text


class Image(models.Model):
    title = models.CharField(max_length=200)
    width = models.IntegerField(default=350)
    height = models.IntegerField(default=350)
    document = models.FileField(_("file"), upload_to='static/media/images', validators=[validate_file_extension],
                                help_text="ONLY IMAGES (png,jpg)", blank=True, default=None)

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField(help_text='<b>Renders Pure HTML<b> <br> Insert Images by  src="imagelink" class="img-responsive img-circle margin" style="display:inline" alt="Bird" width="{width}" height="{height}"')
    images = models.ManyToManyField(Image, blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def body_html(self):
        return embed_image(self.text, self.images.all())

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `Post` object is deleted.
    """
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)

@receiver(models.signals.pre_save, sender=Image)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `Post` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Post.objects.get(pk=instance.pk).document
    except Post.DoesNotExist:
        return False

    new_file = instance.document
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

