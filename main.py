import platform as pltf
import os
import time
from models import Inventory, CraftingTable
from config.craftings import craftings
from config.items import items
from exceptions.exceptions import CraftingNotExist, SlotEmpty, SlotNotFound

colors = {
    "back_gray_light": "\033[47m",
    "text_gray_light": "\033[37m",
    "text_gray": "\033[90m",
    "back_gray": "\033[100m",
    "text_white": "\033[97m",
    "back_white": "\033[107m",
    "text_red": "\033[31m",
    "text_green": "\033[32m",
    "text_orange": "\033[33m",
    "text_blue": "\033[34m",
    "text_magenta": "\033[35m",
    "text_cyan": "\033[36m",
    "back_red": "\033[41m",
    "back_green": "\033[42m",
    "back_orange": "\033[43m",
    "back_blue": "\033[44m",
    "back_magenta": "\033[45m",
    "back_cyan": "\033[46m",
    "text_red_light": "\033[91m",
    "text_green_light": "\033[92m",
    "text_yellow": "\033[93m",
    "text_blue_light": "\033[94m",
    "text_magenta_light": "\033[95m",
    "text_cyan_light": "\033[96m",
    "back_red_light": "\033[101m",
    "back_green_light": "\033[102m",
    "back_yellow": "\033[103m",
    "back_blue_light": "\033[104m",
    "back_magenta_light": "\033[105m",
    "back_cyan_light": "\033[106m",
    "text_bold": "\033[1m",
    "text_opacity": "\033[2m",
    "text_cursive": "\033[3m",
    "text_underline": "\033[4m",
    "text_midline": "\033[9m",
    "text_pulse": "\033[5m",
    "reset": "\033[0m",
}

# Define las instancias de Inventory y CraftingTable que van a servir para manejar el inventario y la mesa de crafteo
inventory = Inventory()
crft = CraftingTable(craftings, items, inventory)

# Este es el input que se le va a dar al programa cuando se craftee un objeto
crafting_table = (
    [[None, None], [None, None], [None, None]],
    [[None, None], [None, None], [None, None]],
    [[None, None], [None, None], [None, None]],
)


def clear():
    if pltf.system() == "Linux" or pltf.system() == "Darwin":
        os.system("clear")
    else:
        os.system("cls")


def command(text: str):
    words = text.split()

    cmd = words[0]
    args = words[1:]

    return cmd, args


def main():
    username = input("Ingresa tu Nombre de Usuario: ")
    while True:
        clear()

        # UI Interactivo
        print(f"{colors['text_bold']}Crea herramientas{colors['reset']}")
        for row in range(len(crafting_table)):
            for slot in range(len(crafting_table[row])):
                if crafting_table[row][slot][1] == None:
                    print(f"{colors['back_gray']}[ ]{colors['reset']}", end="")
                else:
                    item_name = crft.get_item(crafting_table[row][slot][1]).name
                    print(
                        f"{colors['back_gray']}[{colors['text_cursive']}{colors['text_bold']}{item_name}{colors['reset']}{colors['back_gray']}]{colors['reset']}",
                        end="",
                    )
            print("")

        print("\n\n")

        print(f"{colors['text_bold']}Inventario de @{username}{colors['reset']}")
        for slot in range(len(inventory.slots)):
            if inventory.slots[slot] == None:
                print(f"{colors['back_gray']}[ ]{colors['reset']}", end="")
            else:
                item_name = inventory.slots[slot].name

                used = inventory.used_slots[slot]
                text = (
                    f"{colors['back_gray']}[{colors['text_cursive']}{colors['text_bold']}{item_name}{colors['reset']}{colors['back_gray']}]{colors['reset']}"
                    if used == False
                    else f"{colors['back_gray']}[{colors['text_pulse']}>{colors['reset']}{colors['back_gray']}{colors['text_cursive']}{colors['text_bold']}{item_name}{colors['reset']}{colors['back_gray']}{colors['text_pulse']}<{colors['reset']}{colors['back_gray']}]{colors['reset']}"
                )
                print(text, end="")
        print("\n\n")

        cmd, args = command(input(f"@{username}> ").lower())  # La linea de comandos

        if cmd.startswith("move"):  # move <slot> <crafting_slot_x> <crafting_slot_y>
            if len(args) == 3:
                inv_slot = int(args[0]) - 1
                crft_slot_x = int(args[1]) - 1
                crft_slot_y = int(args[2]) - 1

                item = inventory.slots[inv_slot]

                if inventory.used_slots[inv_slot] == False:
                    if item != None:
                        for y in range(len(crafting_table)):
                            for x in range(len(crafting_table[y])):
                                if crft_slot_x == x and crft_slot_y == y:
                                    inventory.used_slots[inv_slot] = True
                                    crafting_table[y][x][1] = item.id
                                    crafting_table[y][x][0] = inv_slot
                    else:
                        print(
                            f"{colors['text_red_light']}Este slot está vacio.{colors['reset']}"
                        )
                        time.sleep(3)
                else:
                    print(
                        f"{colors['text_red_light']}Este slot ya está en uso.{colors['reset']}"
                    )
                    time.sleep(3)
        elif cmd.startswith("deselect"):  # deselect <slot>
            if len(args) == 1:
                slot_id = int(args[0]) - 1
                used = inventory.used_slots[slot_id]

                if used == True:
                    inventory.used_slots[slot_id] = False
                    for y in range(len(crafting_table)):
                        for x in range(len(crafting_table[y])):
                            if crafting_table[y][x][0] == slot_id:
                                crafting_table[y][x][0] = None
                                crafting_table[y][x][1] = None
                else:
                    print(
                        f"{colors['text_red_light']}Este slot no está siendo utilizado.{colors['reset']}"
                    )
                    time.sleep(3)
        elif cmd.startswith("give"):  # give <id>
            if len(args) == 1:
                item_id = int(args[0])

                item = crft.get_item(item_id)

                if item != None:
                    inventory.add(item)
                else:
                    print(
                        f"{colors['text_red_light']}Este item no existe.{colors['reset']}"
                    )
                    time.sleep(3)
        elif cmd.startswith("craft"):  # craft
            matrix = []
            for y in range(len(crafting_table)):
                new_row = []
                for x in range(len(crafting_table[y])):
                    new_row.append(crafting_table[y][x][1])

                matrix.append(new_row)

            try:
                crft.craft(matrix)
            except CraftingNotExist:
                print(
                    f"{colors['text_red_light']}Este crafteo no existe.{colors['reset']}"
                )
                time.sleep(3)

            for y in range(len(crafting_table)):
                for x in range(len(crafting_table[y])):
                    crafting_table[y][x][1] = None

            for v in range(len(inventory.used_slots)):
                inventory.used_slots[v] = False
        elif cmd.startswith("drop"):  # drop <slot>
            if len(args) == 1:
                try:
                    if inventory.used_slots[int(args[0]) - 1] == False:
                        inventory.drop(int(args[0]) - 1)
                    else:
                        print(
                            f"{colors['text_red_light']}Este slot está en uso.{colors['reset']}"
                        )
                        time.sleep(3)
                except SlotEmpty:
                    print(
                        f"{colors['text_red_light']}Este slot está vacio.{colors['reset']}"
                    )
                    time.sleep(3)
                except SlotNotFound:
                    print(
                        f"{colors['text_red_light']}Este slot no existe.{colors['reset']}"
                    )
                    time.sleep(3)
        elif cmd.startswith("exit"):
            raise KeyboardInterrupt


if __name__ == "__main__":
    clear()
    try:
        main()
    except KeyboardInterrupt:
        clear()
        print("Bye!")
        time.sleep(1)
        exit()
