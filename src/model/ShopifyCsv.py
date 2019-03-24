class ShopifyCsv(object):
    def __init__(self, handle='', title='Title', body='Description', vendor='', type='', tags='',
                 published='TRUE', option1Name='',
                 option1Value='', option2Name='',
                 option2Value='', option3Name='', option3Value='', variantSKU='1', variantGrams='',
                 variantInventoryTracker='',
                 variantInventoryQty='0', variantInventoryPolicy='deny', variantFulfillmentService='manual', variantPrice='',
                 variantCompareAtPrice='', variantRequiresShipping='', variantTaxable='', variantBarcode='',
                 imageSrc=' ',
                 imagePosition='', imageAltText='', giftCard='FALSE', googleShoppingMPN='', googleShoppingAge='',
                 googleShoppingGender='', googleProduct='',
                 SEOTitle='', SEODescription='', googleShoppingAdWords='', googleShoppingAdWordsLabels='',
                 googleShoppingCondition='', googleShoppingCustomProduct='FALSE', googleShoppingLabel0='',
                 googleShoppingLabel1='', googleShoppingLabel2='', googleShoppingLabel3='', googleShoppingLabel4='',
                 variantImage='', variantWeightUnit='', variantTaxCode='', costPerItem=''):
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
        self.googleShoppingMPN = googleShoppingMPN
        self.googleShoppingAge = googleShoppingAge
        self.googleShoppingGender = googleShoppingGender
        self.googleProduct = googleProduct
        self.SEOTitle = SEOTitle
        self.SEODescription = SEODescription
        self.googleShoppingAdWords = googleShoppingAdWords
        self.googleShoppingAdWordsLabels = googleShoppingAdWordsLabels
        self.googleShoppingCondition = googleShoppingCondition
        self.googleShoppingCustomProduct = googleShoppingCustomProduct
        self.googleShoppingLabel0 = googleShoppingLabel0
        self.googleShoppingLabel1 = googleShoppingLabel1
        self.googleShoppingLabel2 = googleShoppingLabel2
        self.googleShoppingLabel3 = googleShoppingLabel3
        self.googleShoppingLabel4 = googleShoppingLabel4
        self.variantImage = variantImage
        self.variantWeightUnit = variantWeightUnit
        self.variantTaxCode = variantTaxCode
        self.costPerItem = costPerItem