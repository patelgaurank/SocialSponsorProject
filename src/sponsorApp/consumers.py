import json
import asyncio
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from channels.auth import login
from channels.auth import user_logged_in
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer


class alertMessage(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.channel_layer.group_add("uStatus", self.channel_name)
        # await self.channel_layer.group_add("uLoginStatus", self.channel_name)
        # await self.channel_layer.group_add("uLogoutStatus", self.channel_name)
        self.userStatus = self.scope["user"].username
        await self.send({
            "type": "websocket.accept"
        })

    async def user_uStatus(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event["text"]
        })
    #     await StopConsumer()

    # async def user_uLoginStatus(self, event):
    #     await self.send({
    #         "type": "websocket.send",
    #         "text": event["text"]
    #     })
    #     await StopConsumer()

    # async def user_uLogoutStatus(self, event):
    #     await self.send({
    #         "type": "websocket.send",
    #         "text": event["text"]
    #     })
        # await StopConsumer()

    async def websocket_receive(self, event):
        print("receive", event)

    async def websocket_disconnect(self, event):
        # print("disconnected", event)
        await self.channel_layer.group_discard("uStatus", self.channel_name)
        # await self.channel_layer.group_discard("uLoginStatus", self.channel_name)
        # await self.channel_layer.group_discard("uLogoutStatus", self.channel_name)
