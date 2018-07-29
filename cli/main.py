import argparse
import os
import sys
import jinja2

env = jinja2.Environment()

TEMPLATES = ('saas',)


def die(message, code=1):
    print(message, file=sys.stderr)
    sys.exit(code)


def klass_template_directory(p='..', create=True):
    expanded = os.path.abspath(
        os.path.expanduser(
            os.path.expandvars(p)))
    if create and not os.path.exists(expanded):
        os.makedirs(expanded)
    if not os.path.isdir(expanded):
        print("%s is not a directory" % p)
    return expanded


def klass_name_generate(name):
    name = name.replace('_', ' ').replace('-', ' ')
    return "".join([_.capitalize() for _ in name.split(' ') if _ and isinstance(_, str)])


def modname_generate(name):
    name = name.replace(' ', '_').replace('-', '_')
    name = name.strip().lower()
    return f'myapp_{name}'


class Scaffold(object):

    def run(self, cmdargs):
        cmdargs = cmdargs[1:]
        parser = argparse.ArgumentParser(
            prog=f"{sys.argv[0].split(os.path.sep)[-1]} scaffold",
            description=self.__doc__
        )

        parser.add_argument(
            '-t', '--datasourcetype', type=Template, default=Template('saas'),
            help=f"Use a custom datasource type template, can be one of {TEMPLATES}")

        parser.add_argument('-an', '--appname', default=None,
            help="Your app name, e.g. \"py-datasource-service-google-ads\"")

        parser.add_argument(
            '-a', '--abbreviation', default=None,
            help="Abbreviation of the datasource, e.g. \"google-ads\""
                 "This will help to generate the module name, naming style "
                 "please follow the PEP-8 https://www.python.org/dev/peps/pep-0008/?#descriptive-naming-styles")

        parser.add_argument('-d', '--datasource', default=None,
            help="Full name of the datasource, e.g. \"Google PPC Online Advertising\""
                 "This will help to fullfill the document.")

        parser.add_argument('-au', '--author', default=None,
            help="Author name, this will help to fullfill the document.")

        parser.add_argument('-c', '--customclassname', default=None,
            help="Indicates if the customed class name would be used, y/n to turn on/off, if is off, "
                 "all the class name would be uniformed. And if is turned on, the datasource full name(-d) must be "
                 "provided. Datasource name would be used to program the class name, so its format need to be pep-8 friendly.")

        if not cmdargs:
            sys.exit(parser.print_help())

        args = parser.parse_args(args=cmdargs)

        if not args.abbreviation:
            die('Please provide an Datasource Abbr. e.g. -a google_ads')

        if args.customclassname in ['1', 1, 'y', 'yes']:
            if not args.datasource:
                die('Please provide datasouece(-d) full name to custom the class name.')

        modname = modname_generate(args.abbreviation)

        params = {
            'modname': modname or 'myapp',
            'author': args.author or 'Unknown',
            'appname': args.appname or 'please fullfill your app name here e.g. py-datasource-service-google-ads',
            'classname': klass_name_generate(args.datasource) if
            args.customclassname in ['1', 1, 'y', 'yes'] and args.datasource else 'Datasource'
        }
        args.datasourcetype.render_to(modname, params)


class Template(object):
    def __init__(self, identifier='saas'):
        if identifier not in TEMPLATES:
            die(f"Template \'{identifier}\' is not supported, supported templates: {TEMPLATES}")

        identifier = os.path.join('templates', identifier)
        self.path = os.path.join(os.path.split(os.path.realpath(__file__))[0], identifier)
        self.topfiles_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'templates','top')
        if os.path.isdir(self.path):
            return
        die(f"{identifier} is not a valid module template")

    def files(self):
        for root, _, files in os.walk(self.path):
            for f in files:
                path = os.path.join(root, f)
                yield path, open(path, 'rb').read()

    def top_files(self):
        for root, _, files in os.walk(self.topfiles_path):
            for f in files:
                path = os.path.join(root, f)
                yield path, open(path, 'rb').read()

    def render_to(self, modname, params=None):
        for path, content in self.files():
            local = os.path.relpath(path, self.path)
            root, ext = os.path.splitext(local)
            if ext == '.template':
                local = root

            dest = os.path.join('.', modname, local)
            destdir = os.path.dirname(dest)

            if not os.path.exists(destdir):
                os.makedirs(destdir)

            with open(dest, 'wb') as f:
                if ext not in ('.py', '.html', '.template'):
                    f.write(content)
                else:
                    env.from_string(content.decode('utf-8')).stream(params or {}).dump(f, encoding='utf-8')

        for tpath, tcontent in self.top_files():
            tlocal = os.path.relpath(tpath, self.topfiles_path)
            troot, text = os.path.splitext(tlocal)
            if text == '.template':
                tlocal = troot

            tdest = os.path.join('.', tlocal)
            tdestdir = os.path.dirname(tdest)

            if not os.path.exists(tdestdir):
                os.makedirs(tdestdir)

            with open(tdest, 'wb') as f:
                if text not in ('.py', '.html', '.template'):
                    f.write(tcontent)
                else:
                    env.from_string(tcontent.decode('utf-8')).stream(params or {}).dump(f, encoding='utf-8')


COMMANDS = {
    'scaffold': Scaffold
    ,
}


def main():
    args = sys.argv[1:]
    if not len(args) > 0:
        die(f'Please input an command: {",".join(COMMANDS.keys())}')
    if args[0] not in COMMANDS:
        die(f'Command \'{args[0]}\' is not supported, supported commands: {",".join(COMMANDS.keys())}')

    COMMANDS[args[0]]().run(args)


if __name__ == '__main__':
    main()