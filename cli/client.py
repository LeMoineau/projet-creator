
"""
Ajoute le dossier parent aux url de recherche de package

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

ou

import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

On peut après ça faire des import dans le package parent ou dans le package courant

example:
- PAO
 - cli
    cli.py
    test.py
 - site_sources
    arte_tv.py

# cli.py
from site_sources import arte_tv
from test import coucou
"""

import os, sys; sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from cli.parser import Parser
from cli.printer import Printer
from cli import utils

from colorama import Fore, Style

class Client():
   def __init__(self, parser):
      self.parser = parser
      self.printer = Printer()
      self.current_node_selected = None

   def run(self):
      self.printer.print_title()
      self.printer.print_help()

   def help(self):
      self.printer.print_help()

if __name__ == "__main__":
   parser = Parser()
   parser.init()
   client = Client(parser)
   client.run()

   """
   Forme commandes

   aides:
   python3 main.py -h
   
   interface graphique:
   python main.py gui

   terminal:
   python main.py cli (-s <site>)
   -> si pas -s, demande site
   -> site.init()
   -> affiche liste enfant + revenir en arriere (.. = 0) avec id pour parcourir
   cd 1
   cd 0
   cd 4
   -> en fonction de id, site.crawl_<type node>
   -> affiche liste enfant + revenir en arriere avec id pour parcourir
   cd 3
   -> si <type_node> de selected = Video
   -> affiche formats + revenir en arriere
   -> si format selected, dl la video

   terminal, dois pouvoir:
   - naviguer dans arbre (cd)
   - avoir infos de node (info)
   - rechercher sur le site courant (search)
   - dl video (dl)

   checker tqdm pour faire progress bar (https://stackoverflow.com/questions/3173320/text-progress-bar-in-terminal-with-block-characters)
   """