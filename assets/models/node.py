import uuid
from django.db import models, transaction


class Node(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    key = models.CharField(unique=True, max_length=64)  # '1:1:1:1'
    value = models.CharField(max_length=128)
    child_mark = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)

    is_node = True
    _assets_amount = None
    _full_value_cache_key = '_NODE_VALUE_{}'
    _assets_amount_cache_key = '_NODE_ASSETS_AMOUNT_{}'

    class Meta:
        verbose_name = "节点"
        ordering = ['id']

    def __str__(self):
        return self.value

    @property
    def name(self):
        return self.value

    @property
    def assets_amount(self):
        """
        获取节点下所有资产数量速度太慢，所以需要重写，使用cache等方案
        :return:
        """
        if self._assets_amount is not None:
            return self._assets_amount
        assets_amount = self.get_all_assets().count()
        return assets_amount

    @property
    def parent_key(self):
        parent_key = ":".join(self.key.split(":")[:-1])
        return parent_key

    @property
    def level(self):
        return len(self.key.split(':'))

    @classmethod
    def root(cls):
        root = cls.objects.filter(key__regex=r'^[0-9]+$')
        if root:
            return root[0]
        else:
            return cls.create_root_node()

    @classmethod
    def create_root_node(cls):
        with transaction.atomic():
            return cls.default_node()

    @classmethod
    def default_node(cls):
        defaults = {'value': 'Default'}
        obj, created = cls.objects.get_or_create(defaults=defaults, key='1')
        return obj

    def is_root(self):
        if self.key.isdigit():
            return True
        else:
            return False

    @property
    def parent(self):
        if self.is_root():
            return self
        try:
            parent = self.__class__.objects.get(key=self.parent_key)
            return parent
        except Node.DoesNotExist:
            return self.__class__.root()

    @parent.setter
    def parent(self, parent):
        if not self.is_node:
            self.key = parent.key + ':fake'
            return
        children = self.get_all_children()
        old_key = self.key
        with transaction.atomic():
            self.key = parent.get_next_child_key()
            for child in children:
                child.key = child.key.replace(old_key, self.key, 1)
                child.save()
            self.save()

    def get_children(self, with_self=False):
        pattern = r'^{0}$|^{0}:[0-9]+$' if with_self else r'^{0}:[0-9]+$'
        return self.__class__.objects.filter(key__regex=pattern.format(self.key))

    def get_all_children(self, with_self=False):
        pattern = r'^{0}$|^{0}:' if with_self else r'^{0}:'
        return self.__class__.objects.filter(key__regex=pattern.format(self.key))

    def get_next_child_preset_name(self):
        name = "新节点"
        values = [
            child.value[child.value.rfind(' '):]
            for child in self.get_children()
            if child.value.startswith(name)
        ]
        values = [int(value) for value in values if value.strip().isdigit()]
        count = max(values) + 1 if values else 1
        return '{} {}'.format(name, count)

    def create_child(self, value, _id=None):
        with transaction.atomic():
            child_key = self.get_next_child_key()
            child = self.__class__.objects.create(key=child_key, value=value)
            return child

    def get_next_child_key(self):
        mark = self.child_mark
        self.child_mark += 1
        self.save()
        return "{}:{}".format(self.key, mark)

    def as_tree_node(self):
        from ..tree import TreeNode
        from assets.serializers.node import NodeSerializer
        name = '{} ({})'.format(self.value, self.assets_amount)
        node_serializer = NodeSerializer(instance=self)
        data = {
            'id': self.key,
            'name': name,
            'title': name,
            'pId': self.parent_key,
            'isParent': True,
            'open': self.is_root(),
            'meta': {
                'node': node_serializer.data,
                'type': 'node'
            }
        }
        tree_node = TreeNode(**data)
        return tree_node

    def get_all_assets(self):
        from .asset import Asset
        pattern = r'^{0}$|^{0}:'.format(self.key)
        args = []
        kwargs = {}
        if self.is_root():
            args = []
        else:
            kwargs['nodes__key__regex'] = pattern
        assets = Asset.objects.filter(*args, **kwargs).distinct()
        return assets
