from rest_framework import viewsets


class GenericViewMixin(viewsets.ViewSet):
    service_class = None
    lookup_field = "pk"
    lookup_url_kwarg = None

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_class(self):
        assert self.serializer_class is not None, (
                "'%s' should either include a `serializer_class` attribute, "
                "or override the `get_serializer_class()` method." % self.__class__.__name__
        )

        return self.serializer_class

    def get_serializer_context(self):
        return {"request": self.request, "format": self.format_kwarg, "view": self}

    def get_service_class(self):
        assert self.service_class is not None, (
                "'%s' should either include a `service_class` attribute, "
                "or override the `get_service_class()` method." % self.__class__.__name__
        )
        pass

    def get_service(self, *args):
        service_class = self.get_service_class()
        return service_class(*args)

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                "Expected view %s to be called with a URL keyword argument "
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                "attribute on the view correctly." % (self.__class__.__name__, lookup_url_kwarg)
        )
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        print(filter_kwargs)
