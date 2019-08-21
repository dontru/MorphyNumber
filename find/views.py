from django.shortcuts import render
from django.views import View

from .models import Player


class ResultsView(View):
    def get(self, request, player_1='Paul Morphy', player_2=''):
        context = {
            'player_1': player_1,
            'player_2': player_2,
        }

        type_, chess_player_1 = self.get_chess_player(player_1)
        if type_ == 'Err':
            context['close_matches'] = chess_player_1
            return render(request, 'find/cannot_find_1.html', context)

        type_, chess_player_2 = self.get_chess_player(player_2)
        if type_ == 'Err':
            context['close_matches'] = chess_player_2
            return render(request, 'find/cannot_find_2.html', context)

        return render(request, 'find/results.html', context)

    def get_chess_player(self, player):
        possibilities = self.get_possibilities(player)

        for possibility in possibilities:
            query = Player.objects.filter(**possibility)
            count = query.count()
            if count == 1:
                return 'Ok', query[0]
            elif count > 1:
                return 'Err', list(query[:16])
        else:
            return 'Err', []

    def get_possibilities(self, player):
        player = ' '.join(player.split())
        if len(player) == 0:
            return []

        commas = sum([c == ',' for c in player])
        possibilities = []

        if commas != 1:
            player = ''.join(c for c in player if c != ',')
            words = player.split()
            if len(words) == 1:
                possibilities.append({'last_name': words[0]})
                possibilities.append({'first_name': words[0]})
            else:
                possibilities.append({'first_name': ' '.join(words[0:-1]), 'last_name': words[-1]})
                possibilities.append({'first_name': ' '.join(words[1:]), 'last_name': words[0]})
                possibilities.append({'last_name': words[-1]})
                possibilities.append({'last_name': words[0]})
        else:
            last_name, first_name = player.split(',')
            first_name = ' '.join(first_name.split())
            last_name = ' '.join(last_name.split())
            possibilities.append({'first_name': first_name, 'last_name': last_name})

        return possibilities
