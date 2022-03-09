class FilterWindow:
    def __init__(self,time_window_size,fps):
        self.time_window_size = time_window_size
        self.filter_window = []
        self.fps = fps
        self.window_size = int(self.time_window_size*self.fps)
    def get_filter_window(self,value):
        self.filter_window.append(value)
        if len(self.filter_window)>self.window_size:
            self.filter_window.pop(0)
        return self.filter_window
  