#!/usr/bin/python3
"""Defines Test Cases for `HBNBCommand` Class
"""

import unittest
import re
import os
import sys
from console import HBNBCommand
from models import storage
from models.engine.file_storage import FileStorage
from unittest.mock import patch
from io import StringIO


class TestConsole(unittest.TestCase):
    """Console Unittest Test Cases
    """

    file_path = storage._FileStorage__file_path
    objects = storage._FileStorage__objects
    classes = storage.classes()

    def setUp(self):
        """Sets up any utils
        """
        self.resetStorage()
        self.file_path = storage._FileStorage__file_path
        self.objects = storage._FileStorage__objects
        self.classes = storage.classes()

    def tearDown(self):
        """Clears any test files
        """
        self.resetStorage()

    def resetStorage(self):
        """Clears any data in storage
        """
        objects = {}
        if os.path.isfile(self.file_path):
            os.remove(self.file_path)

    def create_class(self, classname):
        """Creates a class for console tests
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))

        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        return uid

    def test_help(self):
        """Tests `help` command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")

        s = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())

    def test_quit(self):
        """Tests `quit` commmand
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")

        msg = f.getvalue()
        self.assertEqual(len(msg), 6)
        self.assertEqual("Bye..\n", msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit garbage")

        msg = f.getvalue()
        self.assertEqual(len(msg), 6)
        self.assertEqual("Bye..\n", msg)

    def test_EOF(self):
        """Tests `EOF` commmand
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")

        msg = f.getvalue()
        self.assertEqual(len(msg), 7)
        self.assertEqual("\nBye..\n", msg)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF garbage")

        msg = f.getvalue()
        self.assertEqual(len(msg), 7)
        self.assertEqual("\nBye..\n", msg)

    def test_emptyline(self):
        """Tests emptyline functionality
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")

        s = ""
        self.assertEqual(s, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("                  \n")

        s = ""
        self.assertEqual(s, f.getvalue())

    def test_create(self):
        """Tests `create <classname>` command for all classes
        """
        for classname in self.classes:
            self.help_test_create(classname)

    def help_test_create(self, classname):
        """Helper method to test the `create` commmand
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))

        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all {}".format(classname))

        self.assertTrue(uid in f.getvalue())

    def test_create_errors(self):
        """Tests `create` command with errors
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create garbage")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_show(self):
        """Tests `show` command for all classes
        """
        for classname in self.classes:
            self.help_test_show(classname)
            self.help_test_show_advanced(classname)

    def help_test_show(self, classname):
        """Helps test the `show` command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))

        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show {} {}".format(classname, uid))

        s = f.getvalue()[:-1]
        self.assertTrue(uid in s)

    def test_show_errors(self):
        """Tests `show` command with errors
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show garbage")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 6524359")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def help_test_show_advanced(self, classname):
        """Helps test `<classname>.show(<id>)` command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))

        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))

        s = f.getvalue()
        self.assertTrue(uid in s)

    def test_show_advanced_errors(self):
        """Tests show command with errors
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".show()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.show()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.show("6524359")')

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_destroy(self):
        """Tests `destroy` for all classes
        """
        for classname in self.classes:
            self.help_test_destroy(classname)
            self.help_test_destroy_advanced(classname)

    def help_test_destroy(self, classname):
        """Helps test the `destroy` command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))

        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy {} {}".format(classname, uid))

        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")

        self.assertFalse(uid in f.getvalue())

    def test_destroy_errors(self):
        """Tests `destroy` command with errors
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy garbage")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 6524359")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def help_test_destroy_advanced(self, classname):
        """Helps test the `destroy` command
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))

        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('{}.destroy("{}")'.format(classname, uid))

        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".all()")

        self.assertFalse(uid in f.getvalue())

    def test_destroy_advanced_errors(self):
        """Tests `destroy()` command with errors
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".destroy()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.destroy()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.destroy("6524359")')

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_all(self):
        """Tests `all` command for all classes
        """
        for classname in self.classes:
            self.help_test_all(classname)
            self.help_test_all_advanced(classname)

    def help_test_all(self, classname):
        """Helps test the `all` command
        """
        uid = self.create_class(classname)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all")

        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all {}".format(classname))

        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

    def test_all_errors(self):
        """Tests `all` command with errors
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all garbage")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def help_test_all_advanced(self, classname):
        """Helps test the `.all()` command
        """
        uid = self.create_class(classname)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("{}.all()".format(classname))

        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertIn(uid, s)

    def test_all_advanced_errors(self):
        """Tests `all()` command with errors
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.all()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_count_all(self):
        """Tests `count` for all classes
        """
        self.resetStorage()
        for classname in self.classes:
            self.help_test_count(classname)

    def help_test_count(self, classname):
        """Helps test `.count()` command
        """
        for i in range(20):
            uid = self.create_class(classname)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("{}.count()".format(classname))

        s = f.getvalue()[:-1]
        self.assertTrue(len(s) > 0)
        self.assertEqual(s, "22")

    def test_count_errors(self):
        """Tests `.count()` command with errors
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.count()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".count()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

    def test_update(self):
        """Tests `update` command for all classes
        """
        for classname in self.classes:
            attr = "foostr"
            val = "fooval"
            uid = self.create_class(classname)
            cmd = '{}.update("{}", "{}", "{}")'
            cmd = cmd.format(classname, uid, attr, val)

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(cmd)

            s = f.getvalue()
            self.assertEqual(len(s), 0)

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd('{}.show("{}")'.format(classname, uid))

            s = f.getvalue()
            self.assertIn(attr, s)
            self.assertIn(val, s)

    def test_update_errors(self):
        """Tests `update` command with errors
        """
        uid = self.create_class("BaseModel")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update garbage")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel 6534276893 name \"name\"")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel {}'.format(uid))

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('update BaseModel {} name'.format(uid))

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".update()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.update()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update()")

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(
                        "BaseModel.update(6534276893, \"name\", \"name\")"
                    )

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update("{}")'.format(uid))

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** attribute name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('BaseModel.update("{}", "name")'.format(uid))

        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def create_class(self, classname):
        """Creates a class for console tests
        """
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create {}".format(classname))

        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        return uid


if __name__ == "__main__":
    unittest.main()
