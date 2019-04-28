from Product import Product
from ShopifyCsv import ShopifyCsv


def product_to_shopify(product: Product):
    shopifyCsv = ShopifyCsv()
    shopifyCsv.imageSrc = product.image
    shopifyCsv.variantImage = product.imageVariants
    shopifyCsv.handle = product.id
    shopifyCsv.title = product.title
    shopifyCsv.vendor = product.vendor
    shopifyCsv.body = product.details
    shopifyCsv.tags = product.tags
    return shopifyCsv
