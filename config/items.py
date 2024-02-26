class Item:
    def __init__(self, uuid: int, name: str) -> None:
        self.id = uuid
        self.name = name


items = [
    Item(0, "Madera"),
    Item(1, "Diamante"),
    Item(2, "Espada"),
    Item(3, "Doble Espada"),
]
