from django.contrib import admin


class ClickableRowMixin:
    """Makes entire rows clickable in the changelist view."""

    class Media:
        js = ("admin/js/row_click.js",)
