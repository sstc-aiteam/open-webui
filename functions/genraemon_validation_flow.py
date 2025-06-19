import logging
import json
import asyncio

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Callable, Awaitable, Union
from fastapi import Request

from open_webui.models.users import Users
from open_webui.utils.chat import generate_chat_completion
from open_webui.routers.images import image_generations, GenerateImageForm
from open_webui.utils.misc import get_last_user_message


class Pipe:
    class Valves(BaseModel):
        pass

    def __init__(self):
        self.valves = self.Valves()
        self.log = logging.getLogger("GenraVF.pipe")

    async def generate_image(
        self,
        __request__: Request,
        user_prompt: str,
        __user__: dict,
        __event_emitter__: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
    ) -> str:
        await __event_emitter__(
            {
                "type": "status",
                "data": {
                    "description": "Generating image ...",
                    "done": False,
                },
            }
        )

        try:
            images = await image_generations(
                __request__,
                form_data=GenerateImageForm(**{"prompt": user_prompt}),
                user=Users.get_user_by_id(__user__["id"]),
            )

            await __event_emitter__(
                {
                    "type": "status",
                    "data": {
                        "description": "Generated an image",
                        "done": True,
                    },
                }
            )

            for image in images:
                await __event_emitter__(
                    {
                        "type": "message",
                        "data": {"content": f"![Generated Image]({image['url']})"},
                    }
                )

            return f"Notify! the image has been successfully generated"

        except Exception as e:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": f"An error occured: {e}", "done": True},
                }
            )

            return f"Tell the user: {e}"

    async def pipe(
        self,
        body: dict,
        __user__: dict,
        __request__: Request,
        __task__: str | None = None,
        __event_emitter__: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
    ) -> str:
        self.log.info(f"task: {__task__}")
        if __task__ is not None:
            self.log.info(
                f"Ignoring title_generation and tag_generation to spurious addition invocations, task: {__task__}"
            )
            await asyncio.sleep(30)
            return "success"

        self.log.info(f"starting ...")
        self.log.info(f"body: {body}")

        user_prompt = ""
        messages = body.get("messages", [])
        if messages:
            user_prompt = messages[-1]["content"]
        self.log.info(f"user_prompt: {user_prompt}")

        rt = await self.generate_image(
            __request__,
            user_prompt,
            __user__,
            __event_emitter__,
        )

        # body["model"] = "genraemon"
        # user = Users.get_user_by_id(__user__["id"])
        # rt_expansion = await generate_chat_completion(
        #     __request__,
        #     body,
        #     user,
        # )
        # self.log.info(f"Expension prompt: {rt_expansion}")

        await asyncio.sleep(30)
        return rt if rt else "success"
