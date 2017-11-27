# lspt-query
Querying portion of LSPT search engine



Querying->Ranking json format 
<url>/ranking
<url>/stats
{
    'IDENTIFIER_FOR_SEARCH': ____,
    'raw': 
    {
        'raw_search': search_term,
        'raw_tokens': search_tokens
    },
    'transformed': 
    {
        'transformed_search': transformed_search_term,
        'transformed_tokens': transformed_search_tokens,
        'transformed_bigrams': [],
        'transformed_trigrams': [],
    }
}


{
    'result1': ___,
    'result2': ___,
}


