class MouseEvent(object):
	"""
		Prototype
	"""
	def __init__(self, x, y, time_stamp, aoi):
		self.x = x
		self.y = y
		self.time_stamp = time_stamp
		self.aoi = aoi

class BasicMouseEvent(MouseEvent):
	"""
		Mouse event for normal click
	"""
 	def __init__(self, x, y, time_stamp, aoi, is_press):
		super(BasicMouseEvent, self).__init__(x, y, time_stamp, aoi)
		self.is_press = is_press

class DragDropMouseEvent(MouseEvent):

	def __init__(self, x, y, time_stamp, aoi, duration, displacement, drag_start):
		super(DragDropMouseEvent, self).__init__(x, y, time_stamp, aoi)
		self.drag_start = drag_start
		self.duration = duration
		self.displacement = displacement

class DoubleClickMouseEvent(MouseEvent):

    def __init__(self, x, y, time_stamp, aoi, is_first_click):
		super(DoubleClickMouseEvent, self).__init__(x, y, time_stamp, aoi)
		self.is_first_click = is_first_click

class KeyboardEvent():
    def __init__(self, key, time_stamp, aoi):
		self.aoi = aoi
		self.key = key
		self.time_stamp = time_stamp
