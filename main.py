from kivy.app import App
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, StringProperty

from sampleAgent import SampleAgent

# Game constants and rule functions
NEXT_PIT = {  # Usage: NEXT_PIT[player][current_pit]
    1: {
        'A1': 'A2',
        'A2': 'A3',
        'A3': 'A4',
        'A4': 'A5',
        'A5': 'A6',
        'A6': 'AS',
        'AS': 'B1',
        'B1': 'B2',
        'B2': 'B3',
        'B3': 'B4',
        'B4': 'B5',
        'B5': 'B6',
        'B6': 'A1',
    },
    2: {
        'B1': 'B2',
        'B2': 'B3',
        'B3': 'B4',
        'B4': 'B5',
        'B5': 'B6',
        'B6': 'BS',
        'BS': 'A1',
        'A1': 'A2',
        'A2': 'A3',
        'A3': 'A4',
        'A4': 'A5',
        'A5': 'A6',
        'A6': 'B1'
    }
}
NEXT_PLAYER = {
    1: 2,
    2: 1
}


def convert_move_to_pit(player, move):
    if player == 1:
        return 'A' + str(move)
    elif player == 2:
        return 'B' + str(move)
    else:
        raise Exception('convert_move_to_pit: player not valid')


def current_player_get_extra_turn(player, current_pit):
    return (player == 1 and current_pit == 'AS') or (player == 2 and current_pit == 'BS')


def perceive_board(board_state, player):
    if player == 1:
        return board_state
    elif player == 2:
        return {
            'A1': board_state['B1'],
            'A2': board_state['B2'],
            'A3': board_state['B3'],
            'A4': board_state['B4'],
            'A5': board_state['B5'],
            'A6': board_state['B6'],
            'AS': board_state['BS'],
            'B1': board_state['A1'],
            'B2': board_state['A2'],
            'B3': board_state['A3'],
            'B4': board_state['A4'],
            'B5': board_state['A5'],
            'B6': board_state['A6'],
            'BS': board_state['AS'],
        }
    else:
        raise Exception('perceive_board: player not valid')


class MancalaBoard(Widget):
    # Label values to show
    pit_A1 = NumericProperty(0)
    pit_A2 = NumericProperty(0)
    pit_A3 = NumericProperty(0)
    pit_A4 = NumericProperty(0)
    pit_A5 = NumericProperty(0)
    pit_A6 = NumericProperty(0)
    pit_AS = NumericProperty(0)
    pit_B1 = NumericProperty(0)
    pit_B2 = NumericProperty(0)
    pit_B3 = NumericProperty(0)
    pit_B4 = NumericProperty(0)
    pit_B5 = NumericProperty(0)
    pit_B6 = NumericProperty(0)
    pit_BS = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MancalaBoard, self).__init__(**kwargs)
        # initial game's state
        self._board_state = {
            'A1': 4,
            'A2': 4,
            'A3': 4,
            'A4': 4,
            'A5': 4,
            'A6': 4,
            'AS': 0,
            'B1': 4,
            'B2': 4,
            'B3': 4,
            'B4': 4,
            'B5': 4,
            'B6': 4,
            'BS': 0
        }
        self._player_turn = 1
        # Initial game's transient state, the state of animation used while processing the moves
        self._is_turn_processing = True  # True if the engine should process the game, False if waiting player's input
        self._stone_in_hand = 0
        self._current_pit = 'AS'

        # Configure each player's agent here
        self.playerAgentA = SampleAgent()
        self.playerAgentB = SampleAgent()

    def process(self, dt):
        # print(self._board_state)
        # print(self._player_turn)
        # print(self._stone_in_hand)
        self.update_pit_stones()
        if self._is_turn_processing:
            if self._stone_in_hand == 0:
                # No more stone in hand, proceed to the next turn
                self._is_turn_processing = False
                # Check extra turn
                if current_player_get_extra_turn(self._player_turn, self._current_pit):
                    self._player_turn = self._player_turn
                else:
                    self._player_turn = NEXT_PLAYER[self._player_turn]
                # get the player's move
                if self._player_turn == 1:
                    perceived_board_state = perceive_board(self._board_state, self._player_turn)
                    move = self.playerAgentA.makeMove(perceived_board_state, self._player_turn)
                elif self._player_turn == 2:
                    perceived_board_state = perceive_board(self._board_state, self._player_turn)
                    move = self.playerAgentB.makeMove(perceived_board_state, self._player_turn)
                else:
                    raise Exception('player_turn is not valid')
                # process player's move, pick up stones from the selected pit
                self._current_pit = convert_move_to_pit(self._player_turn, move)
                self._stone_in_hand = self._board_state[self._current_pit]
                self._board_state[self._current_pit] = 0
                self._is_turn_processing = True
            else:
                # stones remaining in hand, place the stone into the next pit
                self._current_pit = NEXT_PIT[self._player_turn][self._current_pit]
                self._board_state[self._current_pit] += 1
                self._stone_in_hand -= 1

    def update_pit_stones(self):
        self.pit_A1 = self._board_state['A1']
        self.pit_A2 = self._board_state['A2']
        self.pit_A3 = self._board_state['A3']
        self.pit_A4 = self._board_state['A4']
        self.pit_A5 = self._board_state['A5']
        self.pit_A6 = self._board_state['A6']
        self.pit_AS = self._board_state['AS']
        self.pit_B1 = self._board_state['B1']
        self.pit_B2 = self._board_state['B2']
        self.pit_B3 = self._board_state['B3']
        self.pit_B4 = self._board_state['B4']
        self.pit_B5 = self._board_state['B5']
        self.pit_B6 = self._board_state['B6']
        self.pit_BS = self._board_state['BS']


class MancalaApp(App):
    def __init__(self, **kwargs):
        super(MancalaApp, self).__init__(**kwargs)
        Window.size = (900, 600)
        Builder.load_file('mancala.kv')
        self.mancalaBoard = MancalaBoard()

    def build(self):
        Window.add_widget(self.mancalaBoard)
        Clock.schedule_interval(self.mancalaBoard.process, 1.0 / 2.0)  # set FPS here
        # return self.mancalaBoard


if __name__ == '__main__':
    MancalaApp().run()
