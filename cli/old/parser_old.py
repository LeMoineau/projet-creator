
import os, sys; sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import argcomplete, argparse
import site_sources.enums.enums_urls as enums_urls

class Parser(object):

    def __init__(self, title="Ensemble des commandes du programme TV-replay"):
        self.title = title
        self.parser = argparse.ArgumentParser(description=self.title, epilog="exemples de commandes valides: python3 main.py arte -c plus_vues OU python3 main.py -v <URL> -f 1 ")

    def init(self):
        """
        Initialise le parser pour les arguments
        """
        self._add_args()
        self._apply_parser()

    def _add_args(self):
        """
        Ajoute tous les parametres à la commande d'execution (-s, -c ...etc)
        """
        # optional args
        subparsers = self.parser.add_subparsers()
        tmp_parser = subparsers.add_parser("gui", help=f"ouvrir l'interface graphique")
        tmp_parser.set_defaults(gui=True)

        # create the parser for the "a" command
        self.parser.add_argument("-s", "--site", metavar="SITE", choices=set(enums_urls.urls.keys()), help="site source", nargs=1)
        self.parser.add_argument("-c", "--categorie", metavar="CATEGORIE", 
            help="categorie of videos where search", choices=set([c.key for s in enums_urls.urls.keys() for c in enums_urls.urls[s]]), nargs=1)
        self.parser.add_argument("-v", "--video", metavar="URL", help="url de la video a telecharger", nargs=1)
        self.parser.add_argument("-q", "--query", metavar="STR", help="mot à rechercher", nargs='+')

    def _apply_parser(self):
        """
        Applique les arguments ajouté au parser pour le terminal
        """
        argcomplete.autocomplete(self.parser)
        self.args = vars(self.parser.parse_args())

    def print_help(self):
        """
        Affiche les aides de la commande dans le terminal
        """
        self.parser.print_help()
    
    def get_arg(self, name):
        """
        Renvoie l'argument <name> demandé

        parameters:
        - name: nom de l'argument à renvoyer

        returns:
        - arg: argument de nom <name>
        """
        if name in self.args:
            arg = self.args[name]
            if (isinstance(arg, list) and len(arg) == 1):
                return arg[0]
            return arg
        return None

    def has_arg(self, name):
        """
        Verifie si le parser contient l'argument <name>

        parameters:
        - name: nom de l'argument à verifier

        returns:
        - bool: parser contient l'argument ou non
        """
        return self.get_arg(name) != None

if __name__ == "__main__":
    parser = Parser()
    parser.init()
    parser.print_help()
    print(parser.args)
    print(f"arg 'site': {parser.get_arg('site')}")
    print(f"arg 'query': {parser.get_arg('query')}")
    print(f"arg 'gui': {parser.get_arg('gui')}")