from haystack.query import SQ

def search(sqs, query):
    or_terms = map(lambda x: x.strip(), query.split("OR"))
    final_query = SQ()
    for i, query in enumerate(or_terms):
        if query:
            current_query = SQ()
            # Pull out anything wrapped in quotes and do an exact match on it.
            open_quote_position = None
            non_exact_query = query
            for offset, char in enumerate(query):
                if char == '"':
                    if open_quote_position != None:
                        current_match = non_exact_query[open_quote_position + 1:offset]
                        if current_match:
                            current_query.add(SQ(text__exact=sqs.query.clean(current_match)), SQ.AND)
                        non_exact_query = non_exact_query.replace('"%s"' % current_match, '', 1)
                        open_quote_position = None
                    else:
                        open_quote_position = offset
            
            # Pseudo-tokenize the rest of the query.
            keywords = non_exact_query.split()
            
            # Loop through keywords and add filters to the query.
            for keyword in keywords:
                #exclude = False
                """
                if keyword.startswith('-') and len(keyword) > 1:
                    keyword = keyword[1:]
                    exclude = True
                """
                cleaned_keyword = sqs.query.clean(keyword)
                """
                if exclude:
                    current_query.add(~SQ(text = cleaned_keyword), SQ.AND)
                else:
                """
                current_query.add(SQ(text = cleaned_keyword), SQ.AND)
            final_query.add(current_query, SQ.OR)
    return sqs.filter(final_query)