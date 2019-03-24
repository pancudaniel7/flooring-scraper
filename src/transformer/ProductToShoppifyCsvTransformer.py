from src.model.Product import Product
from src.model.ShopifyCsv import ShopifyCsv


def product_to_shopify(product: Product):
    shoppifyCsv = ShopifyCsv()
    shoppifyCsv.imageSrc = product.image
    shoppifyCsv.variantImage = product.imageVariants
    shoppifyCsv.handle = product.title
    shoppifyCsv.title = product.title
    shoppifyCsv.vendor = product.vendor
    shoppifyCsv.body = product.details
    shoppifyCsv.tags = product.tags
    return shoppifyCsv
