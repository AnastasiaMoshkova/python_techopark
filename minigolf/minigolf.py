class Match:
    def __init__(self, holes, players):
        self._holes = holes
        self._players = players
        self._finished=False
        self._sucsess=False
        self._i=0
        self._hit_player=[]
        self._hit_dict=HitsMatch._start_dict(self._holes)
        self._level=[]
        self._level_list=[]
        self._counter=0
        self._list_name=HitsMatch._playername(players)
        self._list=[]
        self._list_get_table=[]

        self._flag=False
        self._counter_level=0

    @property
    def finished(self):
        return self._finished

    @staticmethod
    def _start_dict(holes):
        hit_dict=[]
        for i in range(holes):
            hit_dict.append([False,0])
        return hit_dict

    @staticmethod
    def _playername(players):
        list_name=[]
        for i in range(len(players)):
            list_name.append(players[i].name)
        return list_name

    def get_table(self):
        self._list.clear()
        list_hit=[]
        for m in range(self._holes):
            if self._hit_dict[m][0]:
                list_hit.append(self._hit_dict[m][1])
            else:
                if self._hit_dict[m][1]>=3:
                    list_hit.append(self._hit_dict[m][1])
                else: list_hit.append(None)

        list_none=[]
        for k in range(self._holes):
            list_none.append(None)
        list_none=tuple(list_none)

        self._list.append(tuple(self._list_name))

        if self._level_list:
            self._list.extend(self._level_list)

        if len(self._level_list)!=self._holes:
            self._list.append(tuple(list_hit))

        for k in range(self._holes-len(self._list)+1):
            self._list.append(list_none)
        self._list_get_table=self._list
        return self._list_get_table

    def get_winners(self):
        if self._finished:
            table_result=[]
            table_result=self.get_table()
            for j in range(self._holes):
                for k in range(self._holes):
                    self._players[j].score+=table_result[k+1][j]
            d_sorted_by_value = sorted(self._players, key=lambda x: x.score)
            new_list=[item.score for item in d_sorted_by_value]
            list_winner=[]
            for k in range(len(self._players)):
                if self._players[k].score==new_list[0]:
                    list_winner.append(self._players[k])
            return list_winner

        else:
            raise RuntimeError

class Player:

    def __init__(self, name):
        self._name = name
        self.score = 0

    @property
    def name(self):
        return self._name

class HitsMatch(Match):

    def hit(self,sucsess=False):
        if len(self._level_list)==self._holes:
            self._finished=True
            raise RuntimeError
        self._sucsess=sucsess
        if self._sucsess:
            self._counter+=1
        while self._hit_dict[self._i][0]:
            self._i+=1
            if self._i==self._holes:
                self._i=0

        self._hit_dict[self._i][1]+=1
        self._hit_dict[self._i][0]=self._sucsess

        if self._hit_dict[self._i][1]==9:
            self._hit_dict[self._i][1]=10
            self._hit_dict[self._i][0]=True
            self._counter+=1

        self._i+=1
        if self._i==self._holes:
            self._i=0

        if self._counter==self._holes:
            for j in range(len(self._hit_dict)):
                self._level.append((self._hit_dict)[j][1])
            level=tuple(self._level)
            self._level.clear()
            self._level_list.append(level)
            self._i=len(self._level_list)
            self._hit_dict=HitsMatch._start_dict(self._holes)
            self._counter=0

        if len(self._level_list)==self._holes:
            self._finished=True


class HolesMatch(Match):
    def hit(self,sucsess=False):
        if len(self._level_list)==self._holes:
            self._finished=True
            raise RuntimeError

        self._sucsess=sucsess

        self._counter_level+=1

        if self._sucsess:
            self._flag=True
            self._hit_dict[self._i][1]=1
            self._hit_dict[self._i][0]=self._sucsess
            self._counter+=1
        else:
            self._hit_dict[self._i][1]=0
            self._hit_dict[self._i][0]=self._flag
            self._counter+=1

        if self._counter==self._holes and not self._flag:
            self._counter=0

        self._i+=1
        if self._i==self._holes:
            self._i=0

        if self._counter_level==10*self._holes and not self._flag:
            for j in range(self._holes):
                self._hit_dict[j][1]=0
                self._hit_dict[j][0]=True
                self._counter=self._holes
                self._flag=True

        if self._counter==self._holes and self._flag:
            for j in range(len(self._hit_dict)):
                self._level.append((self._hit_dict)[j][1])
            level=tuple(self._level)
            self._level.clear()
            self._level_list.append(level)
            self._i=len(self._level_list)
            self._hit_dict=HitsMatch._start_dict(self._holes)
            self._counter=0
            self._counter_level=0
            self._flag=False

        if len(self._level_list)==self._holes:
            self._finished=True
