import aioshoppy
from chat_functions import send_text_to_room


class Command(object):
    def __init__(self, client, store, config, command, room, event):
        """A command made by a user

        Args:
            client (nio.AsyncClient): The client to communicate to matrix with

            store (Storage): Bot storage

            config (Config): Bot configuration parameters

            command (str): The command and arguments

            room (nio.rooms.MatrixRoom): The room the command was sent in

            event (nio.events.room_events.RoomMessageText): The event describing the command
        """
        self.client = client
        self.store = store
        self.config = config
        self.command = command
        self.room = room
        self.event = event
        self.args = self.command.split()[1:]

        # api_key = "ULkxXSwVfLpRxdeTn0mtGjx2xh3Y2USTClrgMmjo2mbAPZYewi"

    async def process(self, api_key="ULkxXSwVfLpRxdeTn0mtGjx2xh3Y2USTClrgMmjo2mbAPZYewi"):
        """Process the command"""
        if self.command.startswith("echo"):
            await self._echo()
        elif self.command.startswith("help"):
            await self._show_help()
        # add query and order to list of process commands
        elif self.command.startswith("query"):
            await self._show_query(api_key)
        elif self.command.startswith("order"):
            await self._show_order(api_key)
        else:
            await self._unknown_command()

    async def _echo(self):
        """Echo back the command's arguments"""
        response = " ".join(self.args)
        await send_text_to_room(self.client, self.room.room_id, response)

    async def _show_help(self):
        """Show the help text"""
        if not self.args:
            text = ("Hello, I am a bot made with matrix-nio! Use `help commands` to view "
                    "available commands.")
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "rules":
            text = "These are the rules!"
        elif topic == "commands":
            text = ("Available commands (Prepend '!c help' + $command): "
                    "rules, query, order")
        # add help query and help order
        elif topic == "query":
            text = "Available queries \n" \
                   "Query List"
        elif topic == "order":
            text = "Available orders \n" \
                   "Order List"
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)

    async def _unknown_command(self):
        await send_text_to_room(
            self.client,
            self.room.room_id,
            f"Unknown command '{self.command}'. Try the 'help' command for more information.",
        )

    # _show_query
    async def _show_query(self, api_key):
        shoppy = aioshoppy.client(api_key)
        """Show the query text"""
        if not self.args:
            text = ("What would you like to query? Use `query commands` to view "
                    "available commands.")
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "commands":
            text = "Available commands \n" \
                   "Query list"

        elif topic == "SPLIT QUERY LIST INTO ARRAY":
            text = "ITERATE THROUGH THESE ELIF STATEMENTS UNTIL ALL POSSIBLE QUERY LIST ITEMS ARE POPULATED AS COMMANDS"
        elif topic == "list":
            # text = print(await shoppy.query.list(page= 1))
            text = await shoppy.query.list(page=1)
            # return text
            await shoppy.close()
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)

    # _show_order
    async def _show_order(self, api_key):
        shoppy = aioshoppy.client(api_key)
        """Show the order text"""
        if not self.args:
            text = ("What would you like to order? Use `order commands` to view "
                    "available commands.")
            await send_text_to_room(self.client, self.room.room_id, text)
            return

        topic = self.args[0]
        if topic == "commands":
            text = "Available commands POPULATE ORDER LIST HERE"
        elif topic == "SPLIT ORDER LIST INTO ARRAY":
            text = "ITERATE THROUGH THESE ELIF STATEMENTS UNTIL ALL POSSIBLE ORDER LIST ITEMS ARE POPULATED AS COMMANDS IN CHRONOLOGICAL ORDER"
        else:
            text = "Unknown help topic!"
        await send_text_to_room(self.client, self.room.room_id, text)
