class ShopifyCSV(object):
    def __init__(self, handle, title, body, vendor, type, tags, published, option1Name, option1Value, option2Name,
                 option2Value, option3Name, option3Value, variantSKU, variantGrams, variantInventoryTracker,
                 variantInventoryQty, variantInventoryPolicy, variantFulfillmentService, variantPrice,
                 variantCompareAtPrice, variantRequiresShipping, variantTaxable, variantBarcode, imageSrc,
                 imagePosition, imageAltText, giftCard, SEOTitle, SEODescription, googleShoppingMetaFields,
                 variantImage, variantWeightUnit, variantTaxCode, costPerItem):
        self.handle = handle
        self.title = title
        self.body = body
        self.vendor = vendor
        self.type = type
        self.tags = tags
        self.published = published
        self.option1Name = option1Name
        self.option1Value = option1Value
        self.option2Name = option2Name
        self.option2Value = option2Value
        self.option3Name = option3Name
        self.option3Value = option3Value
        self.variantSKU = variantSKU
        self.variantGrams = variantGrams
        self.variantInventoryTracker = variantInventoryTracker
        self.variantInventoryQty = variantInventoryQty
        self.variantInventoryPolicy = variantInventoryPolicy
        self.variantFulfillmentService = variantFulfillmentService
        self.variantPrice = variantPrice
        self.variantCompareAtPrice = variantCompareAtPrice
        self.variantRequiresShipping = variantRequiresShipping
        self.variantTaxable = variantTaxable
        self.variantBarcode = variantBarcode
        self.imageSrc = imageSrc
        self.imagePosition = imagePosition
        self.imageAltText = imageAltText
        self.giftCard = giftCard
        self.SEOTitle = SEOTitle
        self.SEODescription = SEODescription
        self.googleShoppingMetaFields = googleShoppingMetaFields
        self.variantImage = variantImage
        self.variantWeightUnit = variantWeightUnit
        self.variantTaxCode = variantTaxCode
        self.costPerItem = costPerItem
