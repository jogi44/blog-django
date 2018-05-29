from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe


class Tag(models.Model):
    word = models.CharField(max_length=35)
    slug = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=False)

    def __unicode__(self):
        return self.word

    def __str__(self):
        return self.word


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)
    tags = models.ManyToManyField(Tag, verbose_name='word')

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)


class Rangee(models.Model):
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.CharField(max_length=50)
    author = models.CharField(max_length=200, default='defaulf')
    created_date = models.DateTimeField(
        default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete=models.CASCADE, default='1')

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text

# class User(models.Model):
#      nick = models.CharField(max_length=200)
#      created_date = models.DateTimeField(
#            blank=True, null=True)
#    GENDER_CHOICES = (
#        (u'M', u'Male'),
#        (u'F', u'Female'),
#    )
#    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
#    login = models.CharField(max_length=20)
#    password = models.CharField(max_length=20)
#    picture = models.ImageField(blank=True , null=True, upload_to='photos/%Y/%m/%d')
#   # ranga = models.ForeignKey(Rangee, on_delete=models.CASCADE)


#    def __str__(self):
#        return self.nick

#    def image_tag(self):
# used in the admin site model as a "thumbnail"
#        return mark_safe('<img src="{}" width="150" height="150" />'.format(self.url()))

#    image_tag.short_description = 'Image'
