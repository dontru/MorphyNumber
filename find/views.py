import random

from django.db.models import Q
from django.shortcuts import render
from django.views import View

from .models import Game, Player


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

        morphy_number, games = self.find(chess_player_1, chess_player_2)
        context['morphy_number'] = self.format_morphy_number(morphy_number)
        context["games"] = games

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

    def find(self, chess_player_1, chess_player_2):
        if chess_player_1.pk == chess_player_2.pk:
            return 0, []

        left = [chess_player_1.pk]
        left_mn = [0, 1]
        right = [chess_player_2.pk]
        right_mn = [0, 1]

        while True:
            len_left = len(left_mn)
            len_right = len(right_mn)

            if (len_left < len_right) or (len_left == len_right and left_mn[-1] < right_mn[-1]):

                left_players = list(self.find_opponents(left).exclude(pk__in=left).values_list('pk', flat=True))
                if not left_players:
                    return -1, []
                left.extend(left_players)
                left_mn.append(len(left))

                intersection = set(left_players).intersection(right)
                if intersection:
                    break

            else:

                right_players = list(self.find_opponents(right).exclude(pk__in=right).values_list('pk', flat=True))
                if not right_players:
                    return -1, []
                right.extend(right_players)
                right_mn.append(len(right))

                intersection = set(right_players).intersection(left)
                if intersection:
                    break

        games = []
        center_pk = random.choice(tuple(intersection))

        last = Player.objects.get(pk=center_pk)
        for start, end in reversed(tuple(zip(left_mn, left_mn[1:]))[:-1]):
            matching_games = self.find_games(last, left[start:end])
            game = random.choice(matching_games)
            games.append(game)
            last = game.opponent(last)

        last = Player.objects.get(pk=center_pk)
        for start, end in reversed(tuple(zip(right_mn, right_mn[1:]))[:-1]):
            matching_games = self.find_games(last, right[start:end])
            game = random.choice(matching_games)
            games.insert(0, game)
            last = game.opponent(last)

        return len(games), games

    def find_opponents(self, players):
        black_opponents = Game.objects.filter(white__in=players).values_list('black')
        white_opponents = Game.objects.filter(black__in=players).values_list('white')
        return Player.objects.filter(Q(pk__in=black_opponents) | Q(pk__in=white_opponents))

    def find_games(self, player, opponents):
        games_white = Game.objects.filter(white=player, black__in=opponents)
        games_black = Game.objects.filter(white__in=opponents, black=player)
        return games_white | games_black

    def format_morphy_number(self, morphy_number):
        if morphy_number != -1:
            return str(morphy_number)
        else:
            return "infinity"
