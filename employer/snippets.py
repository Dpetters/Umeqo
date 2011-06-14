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