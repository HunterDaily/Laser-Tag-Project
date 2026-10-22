import pygame
import sys
import psycopg # type: ignore -> Just so we don't have constantly get an import warning.
from SocketManager import SocketManager # Custom networking class.

def playAction(network: SocketManager, redTeam, greenTeam) -> bool:
    return True