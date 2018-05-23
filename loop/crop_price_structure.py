class CropMandiData:
    def __init__(self, **kwargs):
        self.crop_id = kwargs['crop_id']
        self.mandi_id = kwargs['mandi_id']
        self.price_details = []
    
class PriceDetails:
    def __init__(self, **kwargs):
        self.date = kwargs['date']
        self.min_price = kwargs['min_price']
        self.max_price = kwargs['max_price']
        self.avg_price = kwargs['avg_price']
        self.std = kwargs['std']
        self.delta = kwargs['delta']

