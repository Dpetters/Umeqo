from django.conf import settings

from core import messages
from employer import messages as employer_messages

below_header_message_beginning = "<div id='below_header_message_wrapper'><p>"
below_header_message_ending = "</p></div>"

no_students_selected_snippet = below_header_message_beginning + employer_messages.no_students_selected_message + below_header_message_ending
results_message_beginning = "<div id='no_results_block'><strong id='no_results_message'>"
results_message_end = "</strong></div>"
no_filtering_results = results_message_beginning + messages.no_filtering_results + results_message_end
no_students_in_resume_book = results_message_beginning + messages.no_students_in_resume_book + results_message_end

hide_details_link = "<span class='hide_details'>Hide Details&thinsp;&#x25B2;</span>";
show_details_link = "<span class='show_details'>Show Details&thinsp;&#x25bc;</span>"

starred_img = "<img class='starred_img' title='Remove Star' src='" + settings.STATIC_URL + "images/icons/yellow_star.png'/>";
unstarred_img = "<img class='unstarred_img' title='Add Star' src='" + settings.STATIC_URL + "images/icons/blank_star.png'/>";
add_to_resumebook_img = "<img class='add_to_resume_book_img' title='Add to Resume Book' src='" + settings.STATIC_URL + "images/icons/plus.png'/>";
remove_from_resumebook_img = "<img class='remove_from_resume_book_img' title='Remove from Resume Book' src='" + settings.STATIC_URL + "images/icons/cross.png'/>";