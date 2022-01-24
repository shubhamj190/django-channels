import json
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models.signals import post_save
from channels.layers import get_channel_layer
from django.dispatch import receiver
from asgiref.sync import async_to_sync
# Create your models here.

class Pizza(models.Model):
    name=models.CharField(max_length=100)
    price=models.PositiveIntegerField()
    image=models.CharField(max_length=255)

    def __str__(self):
        return self.name


STATUS_CHOICES=(
    ('Order Received', 'Order Recieved'),
    ('Baking', 'Baking'),
    ('Baked', 'Baked'),
    ('Out for delivery', 'Out for delivery'),
    ('Order recived', 'Order recived'),
)

class Order(models.Model):
    pizza=models.ForeignKey(Pizza, on_delete=models.CASCADE)
    user=models.ForeignKey(User,  on_delete=models.CASCADE)
    order_id=models.UUIDField(primary_key = True,default = uuid.uuid4,editable = False)
    amount=models.IntegerField(default=100)
    status=models.CharField(max_length=255, choices=STATUS_CHOICES, default='Order Received')
    date=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)

    @staticmethod
    def get_order_details(order_id):
        instance=Order.objects.get(order_id=order_id)
        data={}
        data['order_id']=str(instance.order_id)
        data['amount']=instance.amount
        data['status']=instance.status

        pregress_percentage=0
        if instance.status == "Order Received":
            pregress_percentage=20
        elif instance.status == "Baking":
            pregress_percentage=40
        elif instance.status == "Baked":
            pregress_percentage=60
        elif instance.status == "Out for delivery":
            pregress_percentage=80
        elif instance.status == "Order recived":
            pregress_percentage=100

        data['progress']=pregress_percentage

        return data
    
@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    if not created:
        channel_layer=get_channel_layer()
        data={}
        data['order_id']=str(instance.order_id)
        data['amount']=instance.amount
        data['status']=instance.status

        pregress_percentage=0
        if instance.status == "Order Received":
            pregress_percentage=20
        elif instance.status == "Baking":
            pregress_percentage=40
        elif instance.status == "Baked":
            pregress_percentage=60
        elif instance.status == "Out for delivery":
            pregress_percentage=80
        elif instance.status == "Order recived":
            pregress_percentage=100

        print('THIS IS FROM ORDER STATUS',json.dumps(data))
        data['progress']=pregress_percentage

        async_to_sync(channel_layer.group_send)(
            'order_%s' % instance.order_id,{
                'type':'order_status',
                'value':json.dumps(data)
            }
            
        )

