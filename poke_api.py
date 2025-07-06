import aiohttp


async def fetch_move_details(move_name):
    url = f"https://pokeapi.co/api/v2/move/{move_name.lower()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None


async def fetch_pokemon_details(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None


async def fetch_species_details(name):
    url = f"https://pokeapi.co/api/v2/pokemon-species/{name.lower()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            return None
