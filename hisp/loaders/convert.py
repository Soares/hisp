from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader, get_template_from_string, find_template_loader, make_origin
from hisp.management import hisper

class Loader(BaseLoader):
    is_usable = True

    def __init__(self, loaders):
        self._loaders = loaders
        self._cached_loaders = []

    @property
    def loaders(self):
        # Resolve loaders on demand to avoid circular imports
        if not self._cached_loaders:
            for loader in self._loaders:
                if isinstance(loader, BaseLoader):
                    self._cached_loaders.append(loader)
                else:
                    self._cached_loaders.append(find_template_loader(loader))
        return self._cached_loaders

    def load_template_source(self, template_name, template_dirs=None):
        for loader in self.loaders:
            try:
               return loader.load_template_source(template_name, template_dirs)
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist(template_name)

    def load_template(self, template_name, template_dirs=None):
        if not template_name.endswith('.hisp'):
            raise TemplateDoesNotExist(template_name)
        source, display_name = self.load_template_source(template_name, template_dirs)
        source = hisper().convert(source)
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
