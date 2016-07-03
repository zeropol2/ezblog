from django.db import models


class Post(models.Model):
    __status_choices = (
        ('public', '공개',),
        ('private', '비공개',),
    )
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=__status_choices, default='public', null=False, blank=False)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', blank=True)

    def __str__(self):
        return '{}: {}'.format(self.pk, self.title)

    class Meta:
        ordering = ['-created_at', '-pk']

    def get_status_choices(self):
        return self.__status_choices

    def is_public_status(self):
        return self.status == 'public'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=30, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.pk, self.name)


class Tag(models.Model):
    name = models.CharField(unique=True, max_length=30, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.pk, self.name)
