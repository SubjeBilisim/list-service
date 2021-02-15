from django.db import models


class SocialList(models.Model):
    created_by_id = models.IntegerField()
    picture = models.ImageField(upload_to="images/")
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)
    view_count = models.IntegerField(default=0)
    def __str__(self):
        return str(self.pk)





class ListFollower(models.Model):

    list = models.ForeignKey(
        SocialList,
        related_name="list",
        on_delete=models.CASCADE,
    )
    list_following_user = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["list", "list_following_user"], name="unique_list_followers"
            )
        ]

        ordering = ["-created"]


