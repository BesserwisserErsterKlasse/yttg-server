from project.globalobjects.server.config import tcp_config
from project.server import YttgProtocol, YttgServer

server: YttgServer = YttgServer(
    protocol=YttgProtocol(header_size=tcp_config.protocol.header_size),
    max_connections=tcp_config.server.max_connections,
    host=tcp_config.server.host,
    port=tcp_config.server.port,
)
