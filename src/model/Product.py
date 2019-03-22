class Product(object):
    def __init__(self, image, imageVariants, title, vendor, product_code, product_type, construction, species, texture,
                 colorTone, style, floorWidth, thickness, length, venner, finish, gloss, edgeStyle, colorVariation,
                 warranty, installationType, weight, country):
        self.image = image
        self.imageVariants = imageVariants
        self.title = title
        self.vendor = vendor
        self.product_code = product_code
        self.product_type = product_type
        self.construction = construction
        self.species = species
        self.texture = texture
        self.colorTone = colorTone
        self.style = style
        self.floorWidth = floorWidth
        self.thickness = thickness
        self.length = length
        self.venner = venner
        self.finish = finish
        self.gloss = gloss
        self.edgeStyle = edgeStyle
        self.colorVariation = colorVariation
        self.warranty = warranty
        self.installationType = installationType
        self.weight = weight
        self.country = country
