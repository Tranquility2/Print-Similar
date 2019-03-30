"""
Server entire point for Print Similar web service
"""
from code.app import Server

server = Server(datafile="words_clean.txt")
app = server.get_app()
