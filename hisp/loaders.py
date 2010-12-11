from django.template import TemplateDoesNotExist
from django.template.loaders.loader import make_origin, get_template_from_string
from django.template.loaders import app_directories
from django.template.loaders import filesystem
from django import settings
from hisp.management.commands.converthisp import Command as Hisp

def load_compiled(loader, template_name, template_dirs=None):
    if not template_name.endswith('.hisp'):
        raise TemplateDoesNotExist
    return super(loader.__class__, loader).load_template(template_name + '.hisp', template_dirs)

def load_convert(self, template_name, template_dirs=None):
    source, display_name = self.load_template_source(template_name, template_dirs)
    source = Hisp().convert(source)
    origin = make_origin(display_name, self.load_template_source, template_name, template_dirs)
    try:
        template = get_template_from_string(source, origin, template_name)
        return template, None
    except TemplateDoesNotExist:
        # If compiling the template we found raises TemplateDoesNotExist, back off to
        # returning the source and display name for the template we were asked to load.
        # This allows for correct identification (later) of the actual template that does
        # not exist.
        return source, display_name

load = load_convert if settings.DEBUG else load_compiled

class RootLoader(filesystem.Loader):
    load_template = load

class AppLoader(app_directories.Loader):
    load_template = load
