import uuid

from django.db import models
from django.contrib.auth.models import User

from .node import Node


def default_node():
    try:
        root = Node.root()
        return root
    except:
        return None


class AppInfo(models.Model):
    app_name = models.CharField("应用名称", max_length=100)
    url = models.CharField("访问地址", max_length=100, null=True, blank=True)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)
    updated_time = models.DateTimeField("修改时间", auto_now=True, null=True)

    class Meta:
        verbose_name = "应用系统"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.app_name


class OperatingSystem(models.Model):
    name = models.CharField("操作系统名称", max_length=100)
    created_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        verbose_name = "操作系统"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Asset(models.Model):

    PLATFORM_CHOICES = (
        ('Linux', 'Linux'),
        ('Unix', 'Unix'),
        ('Windows', 'Windows'),
        ('Other', 'Other'),
    )

    ASSETTYPE_CHOICES = (
        (1, "实体机"),
        (2, "虚拟机"),
        (3, "存储"),
        (4, "交换机")
    )

    ASSETENV_CHOICSE = (
        (1, "生产"),
        (2, "测试"),
    )

    appinfo = models.ForeignKey(AppInfo, verbose_name="应用系统", null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField("主机名", max_length=100, null=True)
    ip = models.CharField("IP地址", max_length=128, db_index=True)
    os = models.ForeignKey(OperatingSystem, verbose_name="操作系统", null=True, blank=True, on_delete=models.CASCADE)
    port = models.IntegerField("端口", default=22, null=True)
    platform = models.CharField("系统平台", max_length=128, choices=PLATFORM_CHOICES, default='Linux')
    assettype = models.IntegerField("资产类型", choices=ASSETTYPE_CHOICES, default=1)
    nodes = models.ForeignKey(Node, verbose_name="节点", default=default_node, related_name='assets', on_delete=models.CASCADE)
    is_formal = models.BooleanField("是否正式环境", choices=ASSETENV_CHOICSE, default=False)

    model = models.CharField("资产型号", max_length=54, null=True, blank=True)
    cpu_model = models.CharField("CPU model", max_length=64, null=True, blank=True)
    cpu_count = models.IntegerField("CPU count", null=True, blank=True)
    cpu_cores = models.IntegerField("CPU cores", null=True, blank=True)
    cpu_vcpus = models.IntegerField("CPU vcpus", null=True, blank=True)
    memory = models.CharField("Memory", max_length=64, null=True, blank=True)
    disk_total = models.CharField("Disk_total", max_length=100, null=True, blank=True)

    created_by = models.ForeignKey(User, verbose_name="创建人", on_delete=models.CASCADE)
    created_time = models.DateTimeField("添加时间", auto_now_add=True)
    updated_time = models.DateTimeField("修改时间", auto_now=True)
    comment = models.CharField("备注", max_length=255, default='', blank=True)

    class Meta:
        verbose_name = "资产"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0.name}(0.ip)'.format(self)

    def support_ansible(self):
        if self.platform in ("Windows", "Other"):
            return False
        else:
            return True

    @property
    def hardware_info(self):
        if self.cpu_count:
            return '{} Core {} {}'.format(
                self.cpu_vcpus or self.cpu_count * self.cpu_cores,
                self.memory, self.disk_total
            )
        else:
            return ''


class UserProfileManager(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    asset = models.ForeignKey(Asset, verbose_name="资产", blank=True, null=True, on_delete=models.CASCADE)
    app = models.ForeignKey(AppInfo, verbose_name="应用", blank=True, null=True, on_delete=models.CASCADE)
    is_admin = models.BooleanField("is_Admin", default=False)
    username = models.CharField("用户名", max_length=50)
    password = models.CharField("密码", max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = "用户信息管理"
        verbose_name_plural = verbose_name

