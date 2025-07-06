load_dotenv("token.env")
intents = discord.Intents.default()
intents.message_content = True
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)