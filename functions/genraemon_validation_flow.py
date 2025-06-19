import logging
import json
import asyncio
import base64
import os
from pathlib import Path
from PIL import Image
import io
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Callable, Awaitable, Union
from fastapi import Request
from open_webui.models.users import Users
from open_webui.routers.images import image_generations, GenerateImageForm
from open_webui.utils.misc import get_last_user_message
from open_webui.config import UPLOAD_DIR, DATA_DIR
from open_webui.models.files import Files


class Pipe:
    class Valves(BaseModel):
        image_generation_timeout: int = Field(
            default=60, description="Timeout for image generation in seconds"
        )
        max_prompt_length: int = Field(
            default=1000, description="Maximum length of user prompt"
        )
        enable_debug_logging: bool = Field(
            default=False, description="Enable debug logging"
        )
        return_base64_images: bool = Field(
            default=True, description="Return images as base64 strings"
        )
        image_quality: int = Field(
            default=85, description="JPEG quality for base64 images (1-100)"
        )
        max_image_size: int = Field(
            default=1024, description="Maximum image dimension for base64"
        )

    def __init__(self):
        self.valves = self.Valves()
        self.log = logging.getLogger("GenraVF.pipe")
        if self.valves.enable_debug_logging:
            self.log.setLevel(logging.DEBUG)

    def _get_image_file_path(self, image_data: dict) -> Optional[str]:
        """Get the local file path for an image from Open WebUI's storage."""
        try:
            # Method 1: Extract file ID from URL
            image_url = image_data.get("url", "")
            if not image_url:
                return None

            # Parse different URL formats Open WebUI might use
            if "/api/v1/files/" in image_url:
                # Extract file ID from URL like: /api/v1/files/{file_id}/content
                file_id = image_url.split("/api/v1/files/")[1].split("/")[0]

                # Get file record from database
                file_record = Files.get_file_by_id(file_id)
                if file_record:
                    return file_record.path

            elif "/cache/image/" in image_url:
                # Extract from cache URL format
                filename = image_url.split("/cache/image/")[1]
                cache_path = os.path.join(DATA_DIR, "cache", "image", filename)
                if os.path.exists(cache_path):
                    return cache_path

            elif "/uploads/" in image_url:
                # Extract from uploads URL format
                filename = image_url.split("/uploads/")[1]
                upload_path = os.path.join(UPLOAD_DIR, filename)
                if os.path.exists(upload_path):
                    return upload_path

            # Method 2: Try common Open WebUI storage locations
            possible_paths = [
                os.path.join(DATA_DIR, "uploads"),
                os.path.join(DATA_DIR, "cache", "images"),
                os.path.join(DATA_DIR, "storage", "images"),
                UPLOAD_DIR,
            ]

            # Extract filename from URL
            url_parts = image_url.split("/")
            filename = url_parts[-1] if url_parts else ""

            for base_path in possible_paths:
                if os.path.exists(base_path):
                    full_path = os.path.join(base_path, filename)
                    if os.path.exists(full_path):
                        return full_path

            self.log.warning(f"Could not find local path for image: {image_url}")
            return None

        except Exception as e:
            self.log.error(f"Error getting image file path: {str(e)}")
            return None

    def _read_image_file(self, file_path: str) -> Optional[bytes]:
        """Read image file from local filesystem."""
        try:
            if not os.path.exists(file_path):
                self.log.error(f"Image file not found: {file_path}")
                return None

            with open(file_path, "rb") as f:
                return f.read()

        except Exception as e:
            self.log.error(f"Error reading image file {file_path}: {str(e)}")
            return None

    def _resize_image_if_needed(self, image_bytes: bytes) -> bytes:
        """Resize image if it's larger than max_image_size."""
        try:
            with Image.open(io.BytesIO(image_bytes)) as img:
                # Check if resize is needed
                if max(img.width, img.height) <= self.valves.max_image_size:
                    return image_bytes

                # Calculate new size maintaining aspect ratio
                ratio = self.valves.max_image_size / max(img.width, img.height)
                new_width = int(img.width * ratio)
                new_height = int(img.height * ratio)

                # Resize image
                resized_img = img.resize(
                    (new_width, new_height), Image.Resampling.LANCZOS
                )

                # Convert to bytes
                output = io.BytesIO()
                # Convert to RGB if necessary (for JPEG)
                if resized_img.mode in ("RGBA", "LA", "P"):
                    resized_img = resized_img.convert("RGB")

                resized_img.save(
                    output,
                    format="JPEG",
                    quality=self.valves.image_quality,
                    optimize=True,
                )
                return output.getvalue()

        except Exception as e:
            self.log.error(f"Error resizing image: {str(e)}")
            return image_bytes  # Return original if resize fails

    def _image_to_base64(self, image_bytes: bytes, original_format: str = None) -> str:
        """Convert image bytes to base64 data URL."""
        try:
            # Resize if needed
            processed_bytes = self._resize_image_if_needed(image_bytes)

            # Determine MIME type
            if original_format:
                mime_type = f"image/{original_format.lower()}"
            else:
                # Default to JPEG after processing
                mime_type = "image/jpeg"

            # Encode to base64
            base64_string = base64.b64encode(processed_bytes).decode("utf-8")

            # Return as data URL
            return f"data:{mime_type};base64,{base64_string}"

        except Exception as e:
            self.log.error(f"Error converting image to base64: {str(e)}")
            return ""

    def _get_image_format_from_path(self, file_path: str) -> str:
        """Get image format from file extension."""
        ext = Path(file_path).suffix.lower()
        format_map = {
            ".jpg": "jpeg",
            ".jpeg": "jpeg",
            ".png": "png",
            ".gif": "gif",
            ".webp": "webp",
            ".bmp": "bmp",
        }
        return format_map.get(ext, "jpeg")

    async def _process_image_to_base64_internal(self, image_data: dict) -> dict:
        """Process a single image to base64 using internal file access."""
        result = {
            "base64": "",
            "url": image_data.get("url", ""),
            "error": None,
            "file_path": None,
        }

        try:
            # Get local file path
            file_path = self._get_image_file_path(image_data)
            if not file_path:
                result["error"] = "Could not locate image file locally"
                return result

            result["file_path"] = file_path

            # Read image file
            image_bytes = self._read_image_file(file_path)
            if not image_bytes:
                result["error"] = "Failed to read image file"
                return result

            # Get image format
            image_format = self._get_image_format_from_path(file_path)

            # Convert to base64
            base64_data = self._image_to_base64(image_bytes, image_format)
            if not base64_data:
                result["error"] = "Failed to convert to base64"
                return result

            result["base64"] = base64_data
            self.log.info(f"Successfully converted image to base64 from {file_path}")

        except Exception as e:
            result["error"] = f"Processing error: {str(e)}"
            self.log.error(f"Error processing image to base64: {str(e)}")

        return result

    async def generate_images_as_base64_internal(
        self,
        request: Request,
        user_prompt: str,
        user: dict,
        __event_emitter__: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
    ) -> List[dict]:
        """Generate images and convert to base64 using internal file access."""

        # Validate prompt
        if not user_prompt or not user_prompt.strip():
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": "Error: Prompt cannot be empty",
                            "done": True,
                        },
                    }
                )
            return []

        # Emit status
        if __event_emitter__:
            await __event_emitter__(
                {
                    "type": "status",
                    "data": {"description": "Generating images...", "done": False},
                }
            )

        try:
            # Get user object
            user_obj = Users.get_user_by_id(user["id"])
            if not user_obj:
                raise ValueError("User not found")

            # Generate images
            images = await asyncio.wait_for(
                image_generations(
                    request,
                    form_data=GenerateImageForm(prompt=user_prompt),
                    user=user_obj,
                ),
                timeout=self.valves.image_generation_timeout,
            )

            if not images:
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": "No images were generated",
                                "done": True,
                            },
                        }
                    )
                return []

            # Update status
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"Processing {len(images)} generated image(s)...",
                            "done": False,
                        },
                    }
                )

            # Process images to base64 using internal access
            processed_images = []
            for i, image in enumerate(images):
                if __event_emitter__:
                    await __event_emitter__(
                        {
                            "type": "status",
                            "data": {
                                "description": f"Converting image {i+1}/{len(images)} to base64...",
                                "done": False,
                            },
                        }
                    )

                processed_image = await self._process_image_to_base64_internal(image)
                processed_images.append(processed_image)

            # Final status
            successful_images = [
                img for img in processed_images if img["base64"] and not img["error"]
            ]
            if __event_emitter__:
                await __event_emitter__(
                    {
                        "type": "status",
                        "data": {
                            "description": f"Successfully processed {len(successful_images)}/{len(images)} images",
                            "done": True,
                        },
                    }
                )

            return processed_images

        except Exception as e:
            error_msg = f"Image generation failed: {str(e)}"
            self.log.error(error_msg, exc_info=True)
            if __event_emitter__:
                await __event_emitter__(
                    {"type": "status", "data": {"description": error_msg, "done": True}}
                )
            return []

    def _format_images_for_response(self, processed_images: List[dict]) -> str:
        """Format processed images for the response."""
        if not processed_images:
            return "No images were generated."

        response_parts = []
        successful_count = 0

        for i, img_data in enumerate(processed_images):
            if img_data["base64"] and not img_data["error"]:
                successful_count += 1
                response_parts.append(
                    f"![Generated Image {successful_count}]({img_data['base64']})"
                )

                # Add debug info if enabled
                if self.valves.enable_debug_logging and img_data.get("file_path"):
                    response_parts.append(f"*Source: {img_data['file_path']}*")
            else:
                # Log error but don't include in response
                self.log.warning(
                    f"Image {i+1} failed: {img_data.get('error', 'Unknown error')}"
                )

        if successful_count == 0:
            return "Failed to process any generated images."

        # Add summary
        if len(processed_images) > 1:
            response_parts.append(
                f"\n*Successfully generated {successful_count} out of {len(processed_images)} images.*"
            )

        return "\n\n".join(response_parts)

    def _extract_user_prompt(self, body: dict) -> str:
        """Extract user prompt from request body."""
        messages = body.get("messages", [])
        if not messages:
            return ""

        last_message = messages[-1]
        content = last_message.get("content", "")

        if isinstance(content, str):
            return content.strip()
        elif isinstance(content, list):
            text_parts = [
                part.get("text", "") for part in content if part.get("type") == "text"
            ]
            return " ".join(text_parts).strip()

        return ""

    async def pipe(
        self,
        body: dict,
        __user__: dict,
        __request__: Request,
        __task__: str | None = None,
        __event_emitter__: Optional[Callable[[Dict[str, Any]], Awaitable[None]]] = None,
    ) -> str:
        """Main pipe function using internal image access."""

        self.log.info(f"Pipe started with task: {__task__}")

        # Skip system tasks
        if __task__ in ["title_generation", "tag_generation"]:
            self.log.info(f"Skipping system task: {__task__}")
            return "Task skipped"

        try:
            # Extract user prompt
            user_prompt = self._extract_user_prompt(body)
            if not user_prompt:
                error_msg = "No user prompt found in the request"
                self.log.warning(error_msg)
                return f"Error: {error_msg}"

            self.log.info(f"Processing prompt: {user_prompt[:100]}...")

            # Generate and process images using internal access
            processed_images = await self.generate_images_as_base64_internal(
                __request__,
                user_prompt,
                __user__,
                __event_emitter__,
            )

            # Format and return response
            response = self._format_images_for_response(processed_images)

            self.log.info(
                f"Pipe completed successfully with {len(processed_images)} images"
            )
            return response

        except Exception as e:
            error_msg = f"Pipe execution failed: {str(e)}"
            self.log.error(error_msg, exc_info=True)
            return f"Error: {error_msg}"
