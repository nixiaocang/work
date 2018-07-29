datadeck-datasource-pyproj-template
================

This is a python scaffold project for quickly building a framework for [Datadeck](https://dashv2.datadeck.com) datasource microservice.

![](https://img.shields.io/github/tag/AnastagiZeno/HelloWorld.svg)

—————————————————————

## About

Currently only some basic functions are available, including but not limited to eureka-registering, web-server, routing. Deeper encapsulation and type checking will be done in the future work. Originally, ~~I have already done some work in this part, but for a junior developer, me. I found that something is beyond the scope that I can reasonably handle. So I remove them~~. But I will keep working on this.

## Requirements
- Python3.6+
- pip3
- Use of virtualenv is highly recommended

## Usage

```bash
$ git clone git@gitlab.com:PtmindDev/datadeck/datadeck-datasource-pyproj-template.git
$ cd datadeck-datasource-pyproj-template
$ virtualenv venv --python=python3.6
$ source venv/bin/activate
$ pip install -r requirements.txt
```

```bash
python datasource-bin scaffold [-h] [-t DATASOURCETYPE] [-an APPNAME] [-a ABBREVIATION] [-d DATASOURCE] [-au AUTHOR] [-c CUSTOMCLASSNAME]
```
e.g. Creating a `twitter ads` datasource project:

```
./datasource-bin scaffold -a twitter -d 'twitter ads' -c yes
```

Then, a new module would added into your project's root directory

```
...
+--myapp_twitter
    +--config
    |   +--client_secret.json
    |   +--preconfigured_dataset.py
    |   +--__init__.py
    |   +--app_config.py
    +--main
    |   +--datasourceobjects
    |   |   +--__init__.py
    |   |   +--credentialobject.py
    |   +--__init__.py
    |   +--datasourceservice
    |   |   +--service.py
    |   |   +--auth.py
    |   |   +--__init__.py
    +--__init__.py
    +--libs
    |   +--logger.py
    |   +--__init__.py
    |   +--test.py
    |   +--decorators.py
    |   +--const.py
    |   +--exceptions.py
    |   +--util.py
    +--templates
    |   +--docs.html
    +--routes
    |   +--service.py
    |   +--auth.py
    |   +--__init__.py
...
wsgi.py
...

```

1. Fullfill the config/app_config.py file to configure the parameters
2. Implement the methods in main/datasourceservice/service.py && auth.py


## Run
Change the default environment parameter in `wsgi.py`
```angular2html
application = make_app(version=os.environ.get('ENV', 'Local'))
```

Or set your environment variable
```angular2html
bash:~$ export ENV="develop"
```
Then
```
python wsgi.py
```

## TODO

- More encapsulations and features

I have write some abstract classes and methods trying to implement the type checking, but there is still some problem with this part and I'm not sure if doing like this is fit for python as it is a dynamiclly typed language. You can look into the `{{your package}}/main/objects/datasourceobjects/*.py`.

```angular2html
class CredentialObject(AbstractObject):

    def __init__(self):
        super(CredentialObject, self).__init__()

    class Field(AbstractObject.Field):
        pass

    _field_types = {
        'instanceTokenDataUpdate': 'bool',
        'instanceTokenKey': 'string',
        'instanceTokenData': 'InstanceTokenObject',
        'accountTokenDataUpdate': 'bool',
        'accountTokenData': 'string'
    }

    @classmethod
    def _get_field_enum_info(cls):
        return {}

    def refresh(self):
        raise NotImplementedError

    def revoke(self):
        raise NotImplementedError

```
`CredentialObject class` defined the data structure you should return to datadeck manager servicer during the oauth process. Calling ```Credential.create_object(your_dict, type_check=True)``` will give you a CredentialObject instance.
but  before this, you need define the `InstanceTokenObject class` in `{{your package}}/main/objects/datasourceobjects/instancetokenobject.py`. first, the module(file) name need to be the same (case-insensitive) with the class name. 
Also, here is another problem I have not solved, you need to modify the `api/typechecker.py` module, around the 123 and 135 lines, uncomment those codes and fill in your module name('myapp_twitter' here).  
    
``` bash
    # TODO importing customized module
    def _type_is_ad_object(self, value_type):
        try:
            mod = importlib.import_module(
                "api.datasourceobjects." + value_type.lower())
            # if not mod:
            #     importlib.import_module(
            #         "{{your module name}}.main.datasourceobjects." + value_type.lower())
            return mod is not None
        except:
            return False

    # TODO importing customized module
    @staticmethod
    def _create_field_object(field_type, data=None):
        mod = importlib.import_module(
            "api.datasourceobjects." + field_type.lower())
        # if not mod:
        #     importlib.import_module(
        #         "{{your module name}}.main.datasourceobjects." + value_type.lower())
        if mod is not None and hasattr(mod, field_type):
            obj = (getattr(mod, field_type))()
            if data is not None:
                obj._set_data(data)
            return obj
        return None
```

- Deployment parts
- CICD


## Links
[Java Interface Document by Xiaopeng](https://gold-resonance-4655.postman.co/collections/2566308-528ac32c-4e0f-4a94-8671-d1631f3df502?workspace=11371731-d224-4432-a58f-7277d421eaa6) 

## Slack
@Bingxing.Kang