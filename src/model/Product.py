class Product(object):
    def __init__(self, image, imageVariants, title, vendor, product_code, product_type, details, tags):
        self.image = image
        self.imageVariants = imageVariants
        self.title = title
        self.vendor = vendor
        self.product_code = product_code
        self.product_type = product_type
        self.details = details
        self.tags = tags
