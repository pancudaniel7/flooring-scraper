from src.model.Product import Product
from src.model.ShoppifyCsv import ShoppifyCsv


def product_to_shopify(product: Product):
    shoppifyCsv = ShoppifyCsv()
    shoppifyCsv.imageSrc = product.image
    shoppifyCsv.variantImage = product.imageVariants
    shoppifyCsv.handle = product.title
    shoppifyCsv.title = product.title
    shoppifyCsv.vendor = product.vendor
    shoppifyCsv.body = product.details
    shoppifyCsv.tags = product.tags
    return shoppifyCsv
