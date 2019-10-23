class Id:
    def __init__(self, value, ref):
        self.value = value
        self.ref = ref
        self.right = None
        self.left = None

    def add_right(self, r_id):
        self.right = r_id

    def add_left(self, l_id):
        self.left = l_id