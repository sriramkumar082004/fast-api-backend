import httpx
from app.core.config import settings


async def remove_background(image_file: bytes, filename: str) -> bytes:
    api_key = settings.REMOVE_BG_API_KEY
    if not api_key:
        raise ValueError("API Key not configured")

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.apyhub.com/processor/image/change-background/file",
            files={"image": (filename, image_file, "image/png")},
            headers={"apy-token": api_key},
            timeout=60.0,
        )
        if response.status_code == 200:
            return response.content
        else:
            error_msg = f"ApyHub Error: {response.status_code}"
            try:
                # Try to parse JSON error
                data = response.json()
                if "message" in data:
                    error_msg += f" - {data['message']}"
                elif "error" in data:
                    err = data["error"]
                    if isinstance(err, dict) and "message" in err:
                        error_msg += f" - {err['message']}"
                    else:
                        error_msg += f" - {err}"
            except:
                # Fallback to text
                error_msg += f" - {response.text[:200]}"

            print(error_msg)
            raise Exception(error_msg)
