from django.template import TemplateDoesNotExist
from hisp.loaders.convert import Loader as Convert
from django.template.loader import make_origin
from hisp.management import hisper

class Loader(Convert):
    def load_template(self, template_name, template_dirs=None):
        if not template_name.endswith('.hisp'):
            raise TemplateDoesNotExist(template_name)
        source, display_name = self.load_template_source(template_name, template_dirs)
        origin = make_origin(display_name, self.load_template_source, template_name, template_dirs)
        return hisper().convert(source), origin
