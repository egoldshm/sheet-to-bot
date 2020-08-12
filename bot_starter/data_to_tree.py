##################################################################
#               copyright Eytan Goldshmidt (2020)                #
#                 part of project SheetToBot                     #
#                       Eytan Goldshmidt                         #
#                     eitntt@gmail.com                           #
##################################################################


from anytree.dotexport import RenderTreeGraph

from bot_starter.CommandNode import CommandNode
from bot_starter.botMenu import create_response, RETURN_MENU_MESSAGE, RETURN_ONE_ASK
from bot_starter.values_to_bot import data_to_bot

from anytree import RenderTree


class generate_commands_tree(data_to_bot) :
    start_node: CommandNode

    def __init__(self) :
        super().__init__()
        self.start_node = CommandNode()
        self.create_sub_commands(self.start_node)

    def __str__(self) :
        result = ""
        for pre, fill, node in RenderTree(self.start_node) :
            result += "\n" + ("%s%s" % (pre, node.name))
        result = "\n".join(result.split("\n")[2 :])
        return result

    def generate_photo(self, file_name) :
        try :
            RenderTreeGraph(self.start_node).to_picture(file_name)
        except :
            print("problem with RenderTreeGraph")

    def create_sub_commands(self, father_node) :
        sub_commands = list(filter(lambda i : i["father_menu"] == father_node.name, self.botMenu.commands))

        commands_by_father_name = list(filter(
            lambda i : (father_node.name == "/start" or i["father_menu"] == father_node.parent.name) and i[
                "name"] == father_node.name, self.botMenu.commands))

        responses = []

        for res in commands_by_father_name :
            responses.append(create_response(res))

        father_node.set_responses(responses)

        keyboard = self.botMenu.menu_by_father(father_node.name)

        if keyboard and father_node.name != "/start" and father_node.parent.name != "/start" :
            keyboard.append([RETURN_MENU_MESSAGE, RETURN_ONE_ASK])
        elif keyboard and father_node.name != "/start" :
            keyboard.append([RETURN_ONE_ASK])

        father_node.keyboard = keyboard

        for command in sub_commands :
            sub_node = CommandNode(command["name"], parent=father_node)
            self.create_sub_commands(sub_node)


if __name__ == "__main__" :
    x = generate_commands_tree()
    x.start_node
