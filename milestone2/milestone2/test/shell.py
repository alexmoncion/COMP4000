import sys, cmd

class Shell(cmd.Cmd):
    intro = 'welcome to the shell. type help or ? to list commands.\n'
    promt = '>>'
    file = None

if __name__ == '__main__':
    Shell().cmdloop()
