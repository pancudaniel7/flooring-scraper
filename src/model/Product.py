class Product(object):
    def __init__(self, id, image, image_variants, title, vendor, code, type, details, tags):
        self.id = id
        self.image = image
        self.imageVariants = image_variants
        self.title = title
        self.vendor = vendor
        self.code = code
        self.type = type
        self.details = details
        self.tags = tags

    def __eq__(self, other):
        return self.title == other.title \
               and self.code == other.code

    def __hash__(self):
        return hash(('title', self.title,
                     'code', self.code))
