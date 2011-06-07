from django.conf import settings

starred_img = "<img title='Remove Star' src='" + settings.STATIC_URL + "images/icons/yellow_star.png'/>";
unstarred_img = "<img title='Add Star' src='" + settings.STATIC_URL + "images/icons/blank_star.png'/>";
add_to_resumebook_img = "<img title='Add to Resume Book' src='" + settings.STATIC_URL + "images/icons/plus.png'/>";
remove_from_resumebook_img = "<img title='Remove from Resume Book' src='" + settings.STATIC_URL + "images/icons/cross.png'/>";