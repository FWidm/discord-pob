class ItemSlot:
    def __init__(self, name, item_id, item, active=False):
        self.name = name
        self.item_id = item_id
        self.item = item
        self.active = bool(active)

    def __repr__(self) -> str:
        return "ItemSlot [name={}; item_id={}; item={}; active={}]".format(self.name, self.item_id, self.item,
                                                                           self.active)
