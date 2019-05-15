class BasicMouseEvent():

    def __init__(self, aoi=None, x=-1, y=-1, is_press=False, timestamp=-1):
		self.aoi = aoi
        self.x  = x
        self.y = y
        self.is_press = is_press
        self.time_stamp = timestamp

class DragDropMouseEvent(BasicMouseEvent):

    def __init__(self, aoi=None, is_drag=False, x=-1, y=-1, is_press=False, timestamp=-1):
        DetectionComponent.__init__(self, aoi, x, y, is_press, timestamp)
        self.is_drag = is_drag
