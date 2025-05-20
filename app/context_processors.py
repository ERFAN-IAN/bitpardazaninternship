from app.sidebar.sidebar_generator import render_sidebar


def sidebar(request):
    user = request.user
    profile_id = getattr(getattr(user, 'profile', None), 'id', None)
    return {
        'sidebar_html': render_sidebar(user, profile_id)
    }
