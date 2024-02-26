from config.items import Item
from config.craftings import Crafting
from exceptions.exceptions import (
    CraftingNotExist,
    InventoryFull,
    SlotEmpty,
    NoItems,
    SlotNotFound,
)


class Inventory:
    def __init__(self) -> None:
        self.slots = [
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ]

        self.used_slots = [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

    def add(self, item: Item, slot: int = None):
        empty_slot = False
        for v in range(
            len(self.slots)
        ):  # Verifica que haya un slot vacio en el inventario
            if self.slots[v] == None:
                empty_slot = True
                break

        if empty_slot == True:
            if slot == None:
                for v in range(len(self.slots)):
                    if self.slots[v] == None:
                        self.slots[v] = item
                        break
                return None
            else:
                if slot < 35:
                    self.slots[slot] = item
                    return None
                else:
                    raise ValueError(
                        "Solo tienes 35 slots en tu inventario. Usa un valor menor a 35 (Puedes usar 0)"
                    )
        else:
            raise InventoryFull

    def drop(self, slot: int):
        if slot < len(self.slots):
            if self.slots[slot] != None:
                self.slots[slot] = None
                return None
            else:
                raise SlotEmpty
        else:
            raise SlotNotFound

    def get(self, id: int):
        for v in range(len(self.slots)):
            if self.slots[v] != None:
                if self.slots[v].id == id:
                    return True
        return False


class CraftingTable:
    def __init__(self, craftings: list, items: list, inventory: Inventory) -> None:
        self.craftings = craftings
        self.items = items
        self.inventory = inventory

    def craft(self, input: list):
        item = None
        for v in range(len(self.craftings)):
            inputs = self.craftings[v].inputs

            if input in inputs:
                item = v
                break

        if item != None:
            crafting_items = []
            for y in range(len(input)):
                for x in range(len(input[y])):
                    if input[y][x] != None:
                        crafting_items.append(input[y][x])

            for i in crafting_items:
                if self.inventory.get(i) == False:
                    raise NoItems

                for x in range(len(self.inventory.slots)):
                    if self.inventory.slots[x] != None:
                        if self.inventory.slots[x].id == i:
                            self.inventory.drop(x)
                            break

            item = self.get_item(self.get_crafting(item).output)

            self.inventory.add(item)

            return item
        else:
            raise CraftingNotExist

    def get_crafting(self, id: int) -> Crafting | None:
        for v in range(len(self.craftings)):
            if self.craftings[v].id == id:
                return self.craftings[v]

        return None

    def get_item(self, id: int) -> Item | None:
        for v in range(len(self.items)):
            if self.items[v].id == id:
                return self.items[v]

        return None
