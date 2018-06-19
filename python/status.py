from mcstatus import MinecraftServer

# If you know the host and port, you may skip this and use MinecraftServer("example.org", 1234)
server = MinecraftServer.lookup("13.70.127.239")p

# 'status' is supported by all Minecraft servers that are version 1.7 or higher.
status = server.status()
data = {
    'minecraft version': status.version.name,
    'current online players':status.players.online
}

