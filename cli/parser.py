
from email.policy import default
import os, sys
from turtle import title; sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import argcomplete, argparse
from colorama import Fore, Style

class Parser(object):

    def __init__(self):
        self.command_title = "projet-creator"
        self.epilog = f'Run "{self.command_title} help <command>" or "{self.command_title} <command> -h" for more information about a command.'
        self.parser = argparse.ArgumentParser(
            prog=f"{self.command_title}",
            description=f"Manage your project development.", 
            usage=f"{self.command_title} <command> [arguments]",
            epilog=self.epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)

    def init(self):
        """
        Initialise le parser pour les arguments
        """
        self._add_args()
        self._apply_parser()

    def _add_args(self):
        """
        Ajoute tous les parametres à la commande d'execution
        """
        
        # # optional args
        # subparsers = self.parser.add_subparsers(description="", title="Available commands", metavar="manage a project")
        # tmp_parser = subparsers.add_parser("create", help=f"ouvrir l'interface graphique")
        # tmp_parser.set_defaults(gui=True)
        # tmp_parser = subparsers.add_parser("add", help=f"lancer l'interface terminal")
        # tmp_parser.set_defaults(cli=True)
        # tmp_parser = subparsers.add_parser("rm", help=f"lancer l'interface terminal")
        # tmp_parser.set_defaults(cli=True)
        # tmp_parser = subparsers.add_parser("global", help=f"lancer l'interface terminal", usage="projet-creator global <command> [arguments]")
        # tmp_parser.set_defaults(cli=True)
        # subsubparser = tmp_parser.add_subparsers(title="testons un titre")
        # tmptmp_parser = subsubparser.add_parser("add", help=f"add a task for all of the project")

        local_project = self.parser.add_subparsers(title='commands', metavar='\033[A')

        create_cmd = local_project.add_parser('create', 
            help='Create a new project repository', 
            usage=f"{self.command_title} create <directory>",
            epilog=self.epilog,)
        create_cmd.set_defaults(create=True)
        create_cmd.add_argument("directory", type=str, nargs="+", help="name of the directory where create the project")

        add_cmd = local_project.add_parser('add', help='Add a task to the project', usage=f"{self.command_title} add <task>", epilog=self.epilog)
        add_cmd.set_defaults(add=True)
        add_cmd.add_argument("task", nargs="*", help="name of the task to be added")
        
        local_project.add_parser('rm', help='Remove a task from the project')
        local_project.add_parser('check', help='Check/Uncheck a task from the project')
        local_project.add_parser('global', help='Manage all of the next projects')
        local_project.add_parser('help', help='Show command help')

        # global_projects = self.parser.add_argument_group('Manage global projects')
        # global_projects.add_argument('global', help='Global projects commands', nargs="*")
        # global_projects.add_argument('global add', help='Add a task for all the next projects', nargs="*")
        # global_projects.add_argument('global rm', help='Remove a task for all the next projects', nargs="*")

        # tmp_parser.description = "coucou les boys"

        # # create the parser for the "a" command
        # self.parser.add_argument("-s", "--site", metavar="SITE", choices=set({}.keys()), help="site source", nargs=1)

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