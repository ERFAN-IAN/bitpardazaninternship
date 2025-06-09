

sidebar = {
    "css": {
        "position": "fixed",
        "top": "0",
        "left": "0",
        "width": "250px",
        "height": "100vh",
        "background": "rgba(255,255,255,0.15)",
        "backdrop-filter": "blur(12px)",
        "-webkit-backdrop-filter": "blur(12px)",
        "box-shadow": "0 8px 32px 0 rgba(31,38,135,0.37)",
        "border-radius": "0 20px 20px 0",
        "border": "1px solid rgba(255,255,255,0.18)",
        "color": "#222",
        "font-family": "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif",
        "padding": "2rem 1rem 1rem 1rem",
        "z-index": "1100",
        "transition": "transform 0.3s ease",
        "overflow-y": "auto",
        "transform": "translateX(-100%)"
    }
}
sidebar_items = {
    "Dashboard": {
        "label": "Dashboard",
        "url": "index",
        "has_args": False,
        "icon": "fa fa-home",
        "icon_style": {"margin-right": "0.5rem"},
        "permissions": ["authenticated"],
        "css": {
            "font-weight": "bold",
            "font-size": "1.1rem",
            "text-decoration": "none",
            "color": "inherit"
        }
    },
    "Authors": {
        "label": "Authors",
        "icon": "fa fa-user",
        "icon_style": {"margin-right": "0.5rem"},
        "css": {"font-weight": "bold"},
        "submenu": [
            {
                "label": "List Authors",
                "url": "home",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Create Author",
                "url": "add_author",
                "has_args": False,
                "permissions": ["group:Operator", "group:Moderator", "group:Admin", "superuser"],
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Author/Book Mixin",
                "url": "authorbookmixin",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Book Count Table",
                "url": "authorbookcount",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Author/Book Tree",
                "url": "author-book-tree",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Author/Book Pie Chart",
                "url": "standalone_pie",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            }
        ],
        "submenu_css": {
            "list-style": "none",
            "padding-left": "1.2rem",
            "margin-top": "0.5rem"
        }
    },
    "Books": {
        "label": "Books",
        "icon": "fa fa-book",
        "icon_style": {"margin-right": "0.5rem"},
        "css": {"font-weight": "bold"},
        "submenu": [
            {
                "label": "List Books",
                "url": "booklist",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"},
            },
            {
                "label": "Edit Book",
                "url": "bookselect",
                "has_args": False,
                "permissions": ["group:Operator", "group:Moderator", "group:Admin", "superuser"],
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "List Categories",
                "url": "bookcategory_list",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Create Category",
                "url": "bookcategory_create",
                "has_args": False,
                "permissions": ["group:Moderator", "group:Admin", "superuser"],
                "css": {"text-decoration": "none", "color": "inherit"}
            }
        ],
        "submenu_css": {
            "list-style": "none",
            "padding-left": "1.2rem",
            "margin-top": "0.5rem"
        }
    },
    "Purchases": {
        "label": "Purchases",
        "icon": "fa fa-shopping-cart",
        "icon_style": {"margin-right": "0.5rem"},
        "css": {"font-weight": "bold"},
        "submenu": [
            {
                "label": "Purchase List",
                "url": "purchaselist",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            }
        ],
        "submenu_css": {
            "list-style": "none",
            "padding-left": "1.2rem",
            "margin-top": "0.5rem"
        },
        "permissions": ["authenticated"]
    },
    "Account": {
        "label": "Account",
        "icon": "fa fa-user-circle",
        "icon_style": {"margin-right": "0.5rem"},
        "css": {"font-weight": "bold"},
        "submenu": [
            {
                "label": "Profile",
                "url": "userprofile",
                "has_args": True,
                "permissions": ["authenticated"],
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Logout",
                "url": "logout",
                "has_args": False,
                "permissions": ["authenticated"],
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Login",
                "url": "login",
                "has_args": False,
                "permissions": ["anonymous"],
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Sign Up",
                "url": "signup",
                "has_args": False,
                "permissions": ["anonymous"],
                "css": {"text-decoration": "none", "color": "inherit"}
            }
        ],
        "submenu_css": {
            "list-style": "none",
            "padding-left": "1.2rem",
            "margin-top": "0.5rem"
        }
    },
    "Contactus": {
        "label": "Contact Us",
        "url": "contactus",
        "has_args": False,
        "icon": "fa fa-envelope",
        "icon_style": {"margin-right": "0.5rem"},
        "permissions": [],
        "css": {
            "font-weight": "bold",
            "font-size": "1rem",
            "text-decoration": "none",
            "color": "inherit",
        }
    },
    "Admin Tools": {
        "label": "Admin Tools",
        "icon": "fa fa-cogs",
        "icon_style": {"margin-right": "0.5rem"},
        "css": {"font-weight": "bold", "color": "#b00"},
        "permissions": ["group:Admin", "superuser"],
        "submenu": [
            {
                "label": "Django Admin",
                "url": "/admin/",
                "has_args": False,
                "permissions": ["superuser"],
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Book Sales Report",
                "url": "book-sales-report",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Book Publication Report",
                "url": "book-publication-report",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            },
            {
                "label": "Authors by Country",
                "url": "authors-by-country-report",
                "has_args": False,
                "css": {"text-decoration": "none", "color": "inherit"}
            }
        ],
        "submenu_css": {
            "list-style": "none",
            "padding-left": "1.2rem",
            "margin-top": "0.5rem"
        }
    },
    "toggleSidebarBtn": {
        "icon": "fa fa-bars",
        "icon_style": {
            "cursor": "pointer",
            "font-size": "1.4rem",
            "color": "#333",
            "padding": "0"
        },
        "id": "toggleSidebarBtn"
    }
}
