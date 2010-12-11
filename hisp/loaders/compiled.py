from django.template import TemplateDoesNotExist
from django.template.loader import BaseLoader, find_template_loader

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
                self._cached_loaders.append(find_template_loader(loader))
        return self._cached_loaders

    def load_template(self, template_name, template_dirs=None):
        if template_name.endswith('.hisp'):
            compiled_name = template_name + '.html'
            for loader in self.loaders:
                try:
                    return loader(compiled_name, template_dirs)
                except TemplateDoesNotExist:
                    pass
            raise TemplateDoesNotExist(compiled_name)
        raise TemplateDoesNotExist(template_name)
