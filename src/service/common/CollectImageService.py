from PIL import Image
from io import BytesIO

from requests import Session

SHOPIFY_MEGA_PIXELS_IMAGE_RESOLUTION_LIMIT = 20000000


def image_resolution_size(img_url: str, session: Session):
    response = session.get(img_url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    return width * height


def filter_img_urls_by_pixels_limit(image_urls: list, pixels_limit: int, session: Session):
    [url for url in image_urls if image_resolution_size(url, session) <= pixels_limit]
