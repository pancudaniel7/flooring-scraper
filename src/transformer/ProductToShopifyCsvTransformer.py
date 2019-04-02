from src.model.Product import Product
from src.model.ShopifyCsv import ShopifyCsv


def product_to_shopify(product: Product):
    shopifyCsv = ShopifyCsv()
    shopifyCsv.imageSrc = product.image
    shopifyCsv.variantImage = product.imageVariants
    shopifyCsv.handle = product.title
    shopifyCsv.title = product.title
    shopifyCsv.vendor = product.vendor
    shopifyCsv.body = product.details
    shopifyCsv.tags = product.tags
    return shopifyCsv
