class MouseEvent(object):
	"""
		Prototype
	"""
	def __init__(self, x, y, time_stamp, left_click, aoi):
		self.x = x
		self.y = y
		self.time_stamp = time_stamp
		self.left_click = left_click
		self.aoi = aoi

class BasicMouseEvent(MouseEvent):
	"""
		Mouse event for normal click
	"""
 	def __init__(self, x, y, time_stamp, aoi, left_click, is_press):
		super(BasicMouseEvent, self).__init__(x, y, time_stamp, left_click, aoi)
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

class KeyboardEvent(object):
    def __init__(self, key, time_stamp):
		self.key = key
		self.time_stamp = time_stamp
