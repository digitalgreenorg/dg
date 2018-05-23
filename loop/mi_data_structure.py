class AggregatorDetail:

    def __init__(self, **kwargs):
        self.id = kwargs['aggregator_id']
        self.name = kwargs['aggregator_name']
        self.mandi_list = []

    def getAggData(self):
        pass

class MandiDetail:

    def __init__(self, **kwargs):
        self.id =kwargs['mandi_id']
        self.name = kwargs['mandi_name']
        self.category = kwargs['mandi_category']
        self.distance = kwargs['mandi_distance']
        self.transport_list = []
        self.gaddidar_list = []

    def getMandiDetail(self):
        pass

class TransportDetail:

    def __init__(self, **kwargs):
        self.id = kwargs['transport_id']
        self.name = kwargs['transport_name']
        self.cost = kwargs['transport_cost']
        self.capacity = kwargs['transport_capacity']

    def getTransportDetail(self):
        pass


class GaddidarDetail:
    
    def __init__(self, **kwargs):
        self.id = kwargs['gaddidar_id']
        self.name = kwargs['gaddidar_name']
        self.phone_no = kwargs['gaddidar_phone_no']

    def getGaddidarDetail(self):
        pass
    

