from sqlalchemy import desc

class FilterBuilder:
    def __init__(self, request_args, clazz):
        self.request_args = request_args
        self.clazz = clazz
        self.query = clazz.query
        self.order_data()
        
    def add_field(self, field, type):
        filter_data = self.request_args.get(field, None, type)

        if filter_data is not None:
            if type == int:
                self.query = self.query.filter(getattr(self.clazz, field) == filter_data)
            elif type == str:
                self.query = self.query.filter(getattr(self.clazz, field).ilike("%%{}%%".format(filter_data)))
    
    def order_data(self):
        
        order_flds = self.request_args.get("order", None, str)

        if order_flds is not None:
            order_flds = order_flds.split(";")
            
            for fld in order_flds:
                fld_name = fld.split(",")[0]
                fld_dire = fld.split(",")[1]

                if fld_dire == "desc":
                    self.query = self.query.order_by(desc(getattr(self.clazz, fld_name)))
                else:
                    self.query = self.query.order_by(getattr(self.clazz, fld_name))