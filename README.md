# lspt-query
Querying portion of LSPT search engine


POST <OUR_URL>/api/stopwords/



Querying->Ranking json format 
{
    'raw': 
    {
        'raw_search': search_term,
        'raw_tokens': search_tokens
    },
    'transformed': 
    {
        'transformed_search': transformed_search_term,
        'transformed_tokens': transformed_search_tokens
    }
}


