import uuid
from django.db import models, transaction


class Node(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    key = models.CharField(unique=True, max_length=64)  # '1:1:1:1'
    value = models.CharField(max_length=128)
    child_mark = models.IntegerField(default=0)
    c_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "节点"
        ordering = ['id']

    def __str__(self):
        return self.value

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

    def get_children(self, with_self=False):
        pattern = r'^{0}$|^{0}:[0-9]+$' if with_self else r'^{0}:[0-9]+$'
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
        from .tree import TreeNode
        from .serializers import NodeSerializer
        # name = '{} ({})'.format(self.value, self.assets_amount)
        name = self.value
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
