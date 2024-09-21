def message_processor(request):
    if request.user.is_authenticated:
        no_msgs = {
            'username': request.user.username,
            'email': request.user.email,
            'profile_picture': request.user.profile.profile_picture
        }
    else:
        no_msgs = {}
    return {
        'messages': no_msgs
    }

