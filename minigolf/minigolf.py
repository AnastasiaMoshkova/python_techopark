class Match():
    def __init__(self, holes, players):
        self._holes = holes
        self._players = players
        self._finished = False
        self._success = False
        self._i = 0
        self._hit_player = []
        self._hits_list = self._start_list(self._holes)
        self._level = []
        self._level_list = []
        self._counter = 0
        self._list_name = self._player_name(players)
        self._list = []
        self._reverse_list = False
        self._flag = False
        self._counter_level = 0
        #self._play_hole()

    @property
    def finished(self):
        return self._finished

    @staticmethod
    def _start_list(holes):
        hit_list = [[False, 0] for i in range(holes)]
        return hit_list

    @staticmethod
    def _player_name(players):
        list_name = [player.name for player in players]
        return list_name

    def _write_result(self):
        self._level = [hits[1] for hits in self._hits_list]
        self._level_list.append(tuple(self._level))
        self._level.clear()
        self._i = len(self._level_list)
        self._hits_list = self._start_list(self._holes)
        self._counter = 0

    def get_table(self):
        self._list.clear()
        list_hit = []
        for hit_value in self._hits_list:
            if hit_value[0]:
                list_hit.append(hit_value[1])
            else:
                list_hit.append(None)

        list_none = [None for k in range(self._holes)]
        self._list.append(tuple(self._list_name))

        if self._level_list:
            self._list.extend(self._level_list)

        if len(self._level_list) != self._holes:
            self._list.append(tuple(list_hit))

        for k in range(self._holes - len(self._list) + 1):
            self._list.append(tuple(list_none))
        return self._list

    #@property
    def get_winners(self):
        reverse_list = self._reverse_list
        if self._finished:
            table_result = []
            table_result = self.get_table()
            for j in range(self._holes):
                for k in range(self._holes):
                    self._players[j].score += table_result[k + 1][j]
            sorted_by_value = sorted(self._players, key=lambda x: x.score, reverse=reverse_list)
            new_list = [item.score for item in sorted_by_value]
            list_winner = []
            for player in self._players:
                if player.score == new_list[0]:
                    list_winner.append(player)
            return list_winner

        else:
            raise RuntimeError

    def _play_hole(self):
        pass

    def hit(self, success=False):

        if self._finished:
            raise RuntimeError

        self._success = success

        self._play_hole()

        if self._counter == self._holes and self._flag:
            self._write_result()
            self._counter_level = 0
            self._flag = False

        if len(self._level_list) == self._holes:
            self._finished = True




class Player:

    def __init__(self, name):
        self._name = name
        self.score = 0

    @property
    def name(self):
        return self._name


class HitsMatch(Match):

    def _play_hole(self):
		self._flag=True
        if self._success:
            self._counter += 1

        while self._hits_list[self._i][0]:
            self._i += 1
            if self._i == self._holes:
                self._i = 0

        self._hits_list[self._i][1] += 1
        self._hits_list[self._i][0] = self._success

        if self._hits_list[self._i][1] == 9:
            self._hits_list[self._i][1] = 10
            self._hits_list[self._i][0] = True
            self._counter += 1

        self._i += 1
        if self._i == self._holes:
            self._i = 0


class HolesMatch(Match):

    def _play_hole(self):

        self._reverse_list = True
        self._counter_level += 1

        if self._success:
            self._flag = True
            self._hits_list[self._i][1] = 1
            self._hits_list[self._i][0] = self._success
            self._counter += 1
        else:
            self._hits_list[self._i][1] = 0
            self._hits_list[self._i][0] = self._flag
            self._counter += 1

        if self._counter == self._holes and not self._flag:
            self._counter = 0

        self._i += 1
        if self._i == self._holes:
            self._i = 0

        if self._counter_level == 10 * self._holes and not self._flag:
            for j in range(self._holes):
                self._hits_list[j][1] = 0
                self._hits_list[j][0] = True
            self._counter = self._holes
            self._flag = True

