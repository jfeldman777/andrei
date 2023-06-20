class Paint:
    BASIC_GREY = 250
    DELTA_GREY = 5
    PLUS_GREY = 5
    MY_YELLOW = "yellow"
    MY_PINK = "pink"
    MY_GREY = "rgb(211,211,211)"
    MY_BLUE = "blue"
    MY_PURPLE =  "#B266FF"
    ENTRY_MAP_CUT = 20


    def __init__(self)->None:
        self.COL = 0
        self.ROW = 0
        return

    def next_row(self,cell):
        self.DELTA_GREY = 0-self.DELTA_GREY
        print(self.DELTA_GREY)
        self.COL = 0
        self.ROW += 1
        self.cell = cell



    def next_cell(self,cell):
        self.cell = cell
        self.COL += 1

    def back_level_right(self)->int:
        return self.BASIC_GREY + self.DELTA_GREY

    def back_level_left(self)->int:
        return self.back_level_right()-self.PLUS_GREY

    def rgb_back_right(self)->str:
        x = self.back_level_right()
        return f"rgb({x},{x},{x})"

    def rgb_back_left(self)->str:
        y = self.back_level_left()
        return f"rgb({y},{y},{y})"

    def rgb_back(self)->str:
        if self.COL == 0:
            return self.rgb_back_left()
        return self.rgb_back_right()

    def color_balance(self):
        if  isinstance(self.cell, int):
            if self.cell < 0:
                return self.MY_PINK
            if self.cell > 0:
                return self.MY_BLUE
        return self.rgb_back()

    def color_rest(self,all_rest):

        print(88,all_rest)
        if all_rest < 0:
            return self.MY_PINK
        if all_rest == 0:
            return self.MY_YELLOW
        return self.rgb_back_right()

    def color_tasks(self,isOut,isPink):
        if isinstance(self.cell,int):
            if isOut:
                if self.cell > 0:
                    return self.MY_PURPLE
                else:
                    return self.MY_GREY
            else:
                if isPink:
                    return self.MY_PINK
                if self.cell > 0:
                    return self.MY_BLUE

        return self.rgb_back()

    def color_needs(self):
        if isinstance(self.cell, int):
            if self.isOut:
                return self.MY_GREY
            else:
                if self.cell > 0:
                    return self.MY_BLUE

        return self.rgb_back()

    def color_entry_map(self):
        if isinstance(self.cell,int):
            if self.cell > self.ENTRY_MAP_CUT:
                return self.MY_PINK
            elif self.cell > 0:
                return self.MY_YELLOW
        return self.rgb_back()





