from django.urls import reverse
from django.db import models


class List(models.Model):
    def get_absolute_url(self):
        return reverse("view_list", args=[self.id])


class Item(models.Model):
    text = models.TextField(default="")
    list = models.ForeignKey(
        List,
        default=None,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ("id",)
        unique_together = ("text", "list")

    def __str__(self):
        return self.text
