from io import BytesIO

from PIL import Image
from requests import Session

SHOPIFY_MEGA_PIXELS_IMAGE_RESOLUTION_LIMIT = 20000000


def image_resolution_size(img_url: str, session: Session):
    response = session.get(img_url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    return width * height


def first_img_url_under_pixel_limit(image_urls: list, pixels_limit: int, session: Session):
    for url in image_urls:
        pixel_resolution = image_resolution_size(url, session)
        if pixel_resolution <= pixels_limit:
            return url
