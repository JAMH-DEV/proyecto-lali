from app.rcon.client import MinecraftRconClient


client = MinecraftRconClient()

response = client.execute("list")

print("Respuesta de Minecraft:")
print(response)