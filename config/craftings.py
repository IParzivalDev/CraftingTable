from .items import Item


class Crafting:
    def __init__(self, uuid: int, output: Item, inputs: list) -> None:
        self.id = uuid
        self.output = output
        self.inputs = inputs


craftings = [
    Crafting(
        0,
        2,
        [
            # Modo 1
            [[1, None, None], [1, None, None], [0, None, None]],
            [[None, 1, None], [None, 1, None], [None, 0, None]],
            [[None, None, 1], [None, None, 1], [None, None, 0]],
            # Modo 2
            [[1, 1, 0], [None, None, None], [None, None, None]],
            [[None, None, None], [1, 1, 0], [None, None, None]],
            [[None, None, None], [None, None, None], [1, 1, 0]],
            # Modo 3
            [[0, 1, 1], [None, None, None], [None, None, None]],
            [[None, None, None], [0, 1, 1], [None, None, None]],
            [[None, None, None], [None, None, None], [0, 1, 1]],
            # Modo 4
            [[1, None, None], [None, 1, None], [None, None, 0]],
            [[0, None, None], [None, 1, None], [None, None, 1]],
        ],
    ),
    Crafting(
        1,
        3,
        [
            # Modo 1
            [
                [None, None, None],
                [None, 2, None],
                [None, 2, None],
            ],
        ],
    ),
]

