class IdMap:
    def __init__(self, min_id, max_id):
        self.all_ids = list(range(min_id, max_id + 1))
        self.unassigned_ids = list(self.all_ids)
        self.assigned_ids = list()

    def set_as_assigned(self, assigned_ids):
        for assigned_id in assigned_ids:
            if assigned_id in self.all_ids and assigned_id not in self.assigned_ids:
                self.assigned_ids.append(assigned_id)
                self.unassigned_ids.remove(assigned_id)

    def to_bit_mask(self):
        output = 0
        for current_id in reversed(self.all_ids):
            bit = int(current_id in self.assigned_ids)
            output = (output << 1) | bit
        return output
