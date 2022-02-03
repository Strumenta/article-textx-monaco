from pygls.server import LanguageServer

server = LanguageServer()
server.start_ws('localhost', 3001)
