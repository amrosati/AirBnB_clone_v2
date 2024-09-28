#!/usr/bin/python3
""" Console Module """
import cmd
import re
import sys
import json
from datetime import datetime

from models import storage
from models.engine import classes, attributes


class HBNBCommand(cmd.Cmd):
    """ Contains the functionality for the HBNB console"""

    # determines prompt for interactive/non-interactive modes
    prompt = '(hbnb) ' if sys.__stdin__.isatty() else ''

    def default(self, line):
        """Catching commands
        """
        self._precmd(line)

    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def _precmd(self, line):
        """Reformat command line for advanced command syntax.

        Usage: <class name>.<command>([<id> [<*args> or <**kwargs>]])
        (Brackets denote optional fields in usage example.)
        """
        match_line = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
        if not match_line:
            return line

        classname = match_line.group(1)
        command = match_line.group(2)
        args = match_line.group(3)

        match_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
        if match_args:
            _id = match_args.group(1)
            params = match_args.group(2)
        else:
            _id = args
            params = False

        attr_val = ""

        if command == 'update' and params:
            match_dict = re.search('^({.*})$', params)
            if match_dict:
                self._update(classname, _id, match_dict.group(1))
                return ""

            match_attr_val = re.search('(?:"([^"]*)")?(?:, (.*))?$', params)
            if match_attr_val:
                attr_val = (match_attr_val.group(1) or "") + " " +\
                        (match_attr_val.group(2) or "")

        command = f"{command} {classname} {_id} {attr_val}"
        self.onecmd(command)
        return command

    def _update(self, classname, _id, params):
        """Updates an instance by dictionary
        """
        params = params.replace("'", '"')
        params_dict: dict = json.loads(params)

        if not classname:
            print('** class name missing **')
            return
        if classname not in classes:
            print('** class doesn\'t exist **')
            return
        if not _id:
            print('** instance id missing **')
            return

        objects = storage.all()
        key = "{}.{}".format(classname, _id)

        try:
            cls_attributes = attributes()[classname]
            for attr, val in params_dict.items():
                if attr in cls_attributes:
                    val = cls_attributes[attr](val)
                setattr(objects[key], attr, val)

            objects[key].save()
        except KeyError:
            print('** no instance found **')
            return

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the HBNB console"""
        print('Bye..')
        return True

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        print('Bye..')
        return True

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def parse_params(self, args):
        """Parses a string into parameters

        Args:
            args (list): Contains parameters for the created object

        Returns:
            dict: Contains key value pairs of the object cls_attributes
        """
        params = {}

        for arg in args:
            key_val = arg.split('=')
            key = key_val[0]
            val = key_val[1]
            if '"' in val:
                val = val[1:-1].replace('_', ' ')
            elif '.' in val:
                val = float(val)
            else:
                val = int(val)
            params[key] = val

        return params

    def do_create(self, args):
        """ Create an object of any class"""
        args = args.split()

        if not args:
            print("** class name missing **")
            return
        elif args[0] not in classes:
            print("** class doesn't exist **")
            return

        params = self.parse_params(args[1:])
        new_instance = classes[args[0]](**params)

        print(new_instance.id)
        new_instance.save()

    def help_create(self):
        """ Help information for the create method """
        print("Creates a class of any type")
        print("[Usage]: create <className>\n")

    def do_show(self, args):
        """ Method to show an individual object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]

        # guard against trailing args
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id
        try:
            print(storage.all(classes[c_name])[key])
        except KeyError:
            print("** no instance found **")

    def help_show(self):
        """ Help information for the show command """
        print("Shows an individual instance of a class")
        print("[Usage]: show <className> <objectId>\n")

    def do_destroy(self, args):
        """ Destroys a specified object """
        new = args.partition(" ")
        c_name = new[0]
        c_id = new[2]
        if c_id and ' ' in c_id:
            c_id = c_id.partition(' ')[0]

        if not c_name:
            print("** class name missing **")
            return

        if c_name not in classes:
            print("** class doesn't exist **")
            return

        if not c_id:
            print("** instance id missing **")
            return

        key = c_name + "." + c_id

        try:
            del storage.all()[key]
            storage.save()
        except KeyError:
            print("** no instance found **")

    def help_destroy(self):
        """ Help information for the destroy command """
        print("Destroys an individual instance of a class")
        print("[Usage]: destroy <className> <objectId>\n")

    def do_all(self, args):
        """ Shows all objects, or all objects of a class"""
        print_list = []

        if args:
            args = args.split(' ')[0]  # remove possible trailing args
            if args not in classes:
                print("** class doesn't exist **")
                return
            objects = storage.all(classes[args])
            for k, v in objects.items():
                print_list.append(str(v))
        else:
            objects = storage.all()
            for k, v in objects.items():
                print_list.append(str(v))

        print(print_list)

    def help_all(self):
        """ Help information for the all command """
        print("Shows all objects, or all of a class")
        print("[Usage]: all <className>\n")

    def do_count(self, args):
        """Count current number of class instances"""
        if not args:
            print('** class name missing **')
            return
        if args not in classes:
            print('** class doesn\'t exist **')
            return

        objects = storage.all().values()
        objects = [obj for obj in objects if args == type(obj).__name__]

        print(len(objects))

    def help_count(self):
        """ """
        print("Usage: count <class_name>")

    def do_update(self, args):
        """ Updates a certain object with new info """
        args = args.split()
        length = len(args)

        if not length:
            print('** class name missing **')
            return
        if args[0] not in classes:
            print('** class doesn\'t exist **')
            return
        if length == 1:
            print('** instance id missing **')
            return
        if length == 2:
            print('** attribute name missing **')
            return
        if length == 3:
            print('** value missing **')
            return

        attr, val = args[2], args[3]

        type_cast = None
        if not re.search('^".*"$', args[3]):
            if '.' in args[3]:
                type_cast = float
            else:
                type_cast = int
        else:
            val = val.replace('"', '')

        key = "{}.{}".format(args[0], args[1])
        objects = storage.all()
        if key not in objects:
            print('** no instance found **')
            return

        cls_attributes = attributes[args[0]]
        if attr in cls_attributes:
            val = cls_attributes[attr](val)
        elif type_cast:
            try:
                val = type_cast(val)
            except ValueError:
                pass

        setattr(objects[key], attr, val)
        objects[key].save()

    def help_update(self):
        """ Help information for the update class """
        print("Updates an object with new information")
        print("Usage: update <className> <id> <attName> <attVal>\n")


if __name__ == "__main__":
    HBNBCommand().cmdloop()
