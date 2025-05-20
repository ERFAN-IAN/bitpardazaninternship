from django.urls import reverse, NoReverseMatch
from .sidebar_config import sidebar, sidebar_items
from .sidebar_utils import check_permissions


def render_sidebar(user, profile_id=None):
    def render_menu_item(item):
        permissions = item.get('permissions', [])
        if not check_permissions(user, permissions):
            return ''

        label = item.get('label', '')
        icon_html = ''

        if 'icon' in item:
            icon_style = '; '.join(f"{k}: {v}" for k, v in item.get('icon_style', {}).items())
            icon_html = f'<i class="{item["icon"]}" style="{icon_style}"></i> '

        if 'submenu' in item:
            submenu_css = '; '.join(f"{k}: {v}" for k, v in item.get('submenu_css', {}).items())
            submenu_html = ''.join(render_menu_item(subitem) for subitem in item['submenu'])
            css = '; '.join(f"{k}: {v}" for k, v in item.get('css', {}).items())
            html = (
                f'<li style="margin-bottom:1rem;">'
                f'<span style="{css}">{icon_html}{label}</span>'
                f'<ul style="{submenu_css}">{submenu_html}</ul>'
                f'</li>'
            )
            return html

        url = item.get('url')
        if url:
            if item.get("has_args") and profile_id:
                try:
                    href = reverse(url, args=[profile_id])
                except NoReverseMatch:
                    href = "#"
            else:
                try:
                    href = reverse(url)
                except NoReverseMatch:
                    href = url if url.startswith('/') else "#"
            css = '; '.join(f"{k}: {v}" for k, v in item.get('css', {}).items())
            html = f'<li><a href="{href}" style="{css}">{icon_html}{label}</a></li>'
            return html

        id_attr = item.get("id", '')
        return (
            f'<li id={id_attr} style="margin-bottom:1rem;">'
            f'<span>{icon_html}{label}</span>'
            f'</li>'
        )

    sidebar_css = '; '.join(f"{k}: {v}" for k, v in sidebar.get('css', {}).items())

    items_html = ''
    for key, item in sidebar_items.items():
        items_html += render_menu_item(item)

    return (
        f'<div id="sidebar" style="{sidebar_css}">'
        f'<nav><ul style="list-style:none;padding:0;margin:0;">{items_html}</ul></nav>'
        f'</div>'
    )
