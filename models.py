class LegoSet:
    def __init__(
        self,
        name,
        set_number,
        status,
        box_number,
        missing_pieces,
        rebuild_progress,
        notes
    ):
        self.name = name
        self.set_number = set_number
        self.status = status
        self.box_number = box_number
        self.missing_pieces = missing_pieces
        self.rebuild_progress = rebuild_progress
        self.notes = notes