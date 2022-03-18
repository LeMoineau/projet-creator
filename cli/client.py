
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
from elements.channels.artetv import ArteTV
from cli import utils
from web.downloader import Downloader
from enums import enum_site

from colorama import Fore, Style

class Client():
   def __init__(self, parser):
      self.parser = parser
      self.printer = Printer()
      self.current_node_selected = None

   def run(self):
      self.printer.print_title()
      self.printer.print_help()
      
      site_arg = self.parser.get_arg("site")
      if not site_arg:
         site_arg = self._selection_site()
         print("")
         
      self.printer.print_message(f"Site source selectionné: {site_arg}", site_arg)
      self.site_class = enum_site[site_arg]["crawler"]()
      self.printer.print_message(f"Choix du crawler {self.site_class.crawler.driverName}", self.site_class.crawler.driverName)
      self.printer.print_message(f"Lancement du crawler {site_arg}...", site_arg)
      self.site_class.init()

      self.current_node_selected = self.site_class

      cmd = "cd"
      while cmd != "exit":
         if "cd" in cmd:
            current_table = self.printer.print_table_node(self.current_node_selected)
         cmd = self.printer.print_input("\nQue voulez-vous faire ?", "#")
         self.process_cmd(cmd, current_table)

      self.site_class.dispose()

   def _selection_site(self):
      list_site = {"arte": ArteTV}
      self.printer.print_message("Liste des sites disponibles:")
      for s, v in enum_site.items():
         self.printer.print_message(f" - {s}: {v['description']}", s)
      return self.printer.print_input("\nDe quel site voulez-vous prendre les videos ?", "site", lambda x: x not in list_site.keys(), "ce site n'est pas dans la liste des sites disponibles")

   def process_cmd(self, cmd, current_table):
      args = cmd.split(" ")
      if args[0] == "cd":
         self.cd(args[1:], current_table)
      elif args[0] == "help":
         self.help()
      elif args[0] == "info":
         self.info(args[1:], current_table)
      elif args[0] == "search":
         self.search(args[1:])
      elif args[0] == "dl":
         self.dl(args[1:], current_table)
      elif args[0] != "exit":
         self.printer.print_error(f'aucune commande trouvée pour "{cmd}"')
         self.printer.print_help()

   def cd(self, args, current_table):
      if len(args) >= 1:
         index = args[0]
         if int(index) in current_table.keys():
            self.current_node_selected = current_table[int(index)]
            if utils.get_node_type(self.current_node_selected) != "Channel" and len(self.current_node_selected.children) <= 0:
               if self.current_node_selected.url == self.site_class.guide_tv:
                  self.guide(args[1:])
               else:
                  getattr(self.site_class, f"crawl_{utils.get_node_type(self.current_node_selected).lower()}")(self.current_node_selected)
         else:
            self.printer.print_error(f"argument invalide, l'id '{index}' n'existe pas")
      else:
         self.printer.print_error(f"commande incorrect, il manque 1 paramètre")
         self.printer.print_warning(f"{Fore.MAGENTA}usage {Style.BRIGHT}cd <id_noeud> {Style.RESET_ALL}")

   def guide(self, args):
      pass

   def info(self, args, current_table):
      if len(args) >= 1:
         index = args[0]
         if int(index) in current_table.keys():
            current_node = current_table[int(index)]
            node_infos = vars(current_node)
            print("\n[Informations de ArteTV]")
            self.printer.print_node_infos(node_infos)
            self.printer.print_message(f"type: {utils.get_node_type(current_node)}", "type")
            if utils.get_node_type(current_node) == "Video":
               ytdl_infos = current_node.extract_infos()
               self.printer.print_message(f"\n[Informations de YoutubeDL]")
               self.printer.print_node_infos(ytdl_infos)
         else:
            self.printer.print_error(f"argument invalide, l'id '{index}' n'existe pas")
      else:
         self.printer.print_error(f"commande incorrect, il manque 1 paramètre")
         self.printer.print_warning(f"{Fore.MAGENTA}usage {Style.BRIGHT}info <id_noeud> {Style.RESET_ALL}")

   def search(self, args):
      pass

   def dl(self, args, current_table):
      if len(args) >= 1:
         index = args[0]
         if int(index) in current_table.keys():
            current_node = current_table[int(index)]
            if utils.get_node_type(current_node) == "Video":
               # Choix nom fichier
               rep = self.printer.print_input("\nVoulez-vous sauvegarder la vidéo sous un nom particulier ? (Y/n)", "#")
               if rep == "Y":
                  filename = self.printer.print_input("\nSous quel nom voulez-vous sauvegarder la vidéo ?", "filename")
               else:
                  filename = None
               # Choix format vidéo
               rep = self.printer.print_input("\nVoulez-vous choisir un format particulier pour la vidéo ? (Y/n)", "#")
               if rep == "Y":
                  formats = current_node.get_formats()
                  id_format = "-1"
                  while int(id_format) < 0 or int(id_format) >= len(formats):
                     self.printer.print_regular_table(formats, ["format_id", "format", "ext"], "Liste des formats disponibles pour la vidéo")
                     id_format = int(self.printer.print_input("\nQuel format voulez-vous choisir ?", "id"))
                     id_format -= 1
                     if int(id_format) < 0 or int(id_format) >= len(formats):
                        self.printer.print_error(f"le format #{id_format+1} n'existe pas, veuillez en choisir un autre")
                     else:
                        self.printer.print_message(f"format selectionné: {formats[int(id_format)]['format']}", formats[int(id_format)]['format'])
                  form = formats[int(id_format)]
               else:
                  form = None
               # Telechargement de la video
               current_node.download(form, filename)
            else:
               self.printer.print_error(f"argument invalide, le noeud #{index} selectionné n'est pas une vidéo")
         else:
            self.printer.print_error(f"argument invalide, l'id '{index}' n'existe pas")
      else:
         self.printer.print_error(f"commande incorrect, il manque 1 paramètre")
         self.printer.print_warning(f"{Fore.MAGENTA}usage {Style.BRIGHT}info <id_noeud> {Style.RESET_ALL}")

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