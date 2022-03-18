
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

from operator import index
import os, sys

from site_sources.enums import enums_site

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from cli.parser import Parser
from site_sources.enums import enums_urls
from cli import utils
from web.downloader import Downloader

class Client():
   def __init__(self, parser):
      self.parser = parser

   def _input(self, message, valueName, condition=lambda x:False, errorMessage = ""):
      """
      Méthode générique pour demander à l'utilisateur d'entrer des informations

      parameters:
      - message: message à afficher avant l'entrée utilisateur
      - valueName: nom de la valuer a entrer pour l'utilisateur
      - condition: (optionnel) condition a remplir pour empecher de sortir de la boucle d'entrée
      - errorMessage: (optionnel) message à afficher si <condition> n'est pas respectée
      """
      print(f"{message}")
      res = None 
      while res == None or len(res) <= 0 or condition(res):
         if res != None:
            print(message if len(errorMessage) <= 0 else errorMessage)
         res = input(f"{valueName}: ")
      return res

   def _selection_categorie(self, site):
      """
      Selection d'une categorie d'un site source pour entré de l'utilisateur

      parameters:
      - site: site source utilisé

      returns:
      - categorie: categorie selectionnée
      """
      categorie = self.parser.get_arg("categorie")

      if categorie == None:
         categorie = self._input(f"\nVeuillez entrer une categorie parmi les suivantes: \n-> {enums_urls.list_of_categories_to_str(site)}", 
            "categorie", lambda x: not enums_urls.key_in_categories(site, x))

      return categorie

   def _selection_film(self, table_data):
      """
      Selectionne un film parmis ceux de la categorie selectionnée

      parameters:
      - table_data: dictionnaire avec clé=id et value=url du film

      returns:
      - url: l'url correspondant au film selectionné par l'id
      """
      index_str = self._input(f"Veuillez entrer l'id du film à télécharger", "id", lambda x: int(x) not in table_data, "l'id entré est invalide")
      return table_data[int(index_str)]

   def _selection_format(self, table_format):
      index_str = self._input(f"Veuillez entrer l'id du format de la video à télécharger", "id", lambda x: int(x) not in table_format, "l'id entré est invalide")
      return table_format[int(index_str)]

   def run(self):
      """
      Fonction maitresse du client qui s'executera après l'entrée de la commande par l'user et 
      qui doit aboutir a un dl d'une video
      """
      site = self.parser.get_arg("site")
      video = self.parser.get_arg("video")

      if site != None:

         query = self.parser.get_arg("query")
         siteClass = enums_site.site_list[site]()
         tree = {}

         if query == None:
            categorie = self._selection_categorie(site)
            tree = siteClass.scrape_categorie(key=categorie)
         else:
            tree = siteClass.search_videos(query)

         table_res = utils.print_table_tree(tree["categories"], ["title", "duree", "image"])
         selected_video = self._selection_film(table_res)

      elif video != None:
         """
         - get infos de la video depuis url
         - stocker dans selected_video
         """
         pass

      dler = Downloader()
      formats = dler.get_formats(selected_video["url"])

      table_format = utils.print_table(formats, ["format", "ext"], "\nFormats\n")
      selected_format = self._selection_format(table_format)

      dler.download_video(selected_video, selected_format)

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
   """