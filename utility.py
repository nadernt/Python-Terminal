class Utility:

    def calculate_combo_width(self, list_items):
        len_max = 0
        for m in list(list_items):
            if len(str(m)) > len_max:
                len_max = len(str(m))

        return len_max