from django.db import models


class Member(models.Model):
    tel = models.CharField(max_length=15, primary_key=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.IntegerField(null=True, blank=True)
    category = models.ManyToManyField("Category", null=True, blank=True)
    status = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    register = models.DateTimeField(auto_now=True)
    send = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.tel)


class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Connection(models.Model):
    connect1 = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, related_name="connector")
    connect2 = models.ForeignKey(Member, null=True, on_delete=models.SET_NULL, related_name="link")
    first = models.DateTimeField(auto_now=True)
    status = models.IntegerField(default=1)

    class Meta:
        unique_together = ('connect1', 'connect2',)

    def __str__(self):
        return "%s<->%s" % (self.connect1.name, self.connect2.name)


class MemberLog(models.Model):
    key = models.CharField(max_length=150)
    value = models.TextField()
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str("{}->{}".format(str(self.member.tel), str(self.key)))


class Message(models.Model):
    event = models.CharField(max_length=100)
    context = models.TextField()
    keyboard = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.event)
