import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .views import get_q, get_active_questions
import time
from .models import Question, Questionset

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print("connected!",event)
        await self.send({
            "type":"websocket.accept"
        })
        await self.send({
            "type":"websocket.send",
            "text":"helo world",
        })
        me = self.scope['user']
        
        
        # for i in range(4):
        msg = "hell0"
        # time.sleep(1)
        objs = await self.get_question()
        # questions = await self.get_a_q
        if objs is not None:
            obj = objs
            while obj!=None:
                curr_obj = obj
                curr_obj_id = curr_obj.pk
                q_time = obj.timelimit
                msg = obj.question 
                obj = Question.objects.get(pk=curr_obj_id+1)

                
                await self.send({
                "type":"websocket.send",
                "text":msg,
            })
                time.sleep(q_time)
        
        print(obj)
        print(me)
    async def websocket_recieve(self,event):
        print("Recieved data!",event)  

    async def websocket_disconnect(self,event):
        print("Disconnected!",event) 

    @database_sync_to_async
    def get_question(self):
        return get_q()

    @database_sync_to_async
    def get_a_q(self):
        return get_active_questions()