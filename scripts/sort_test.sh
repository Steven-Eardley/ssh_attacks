curl -XPOST 'localhost:9200/ssh_attacks/ssh_entry/_search' -d '
{
    "query" :
    {
        "match_all" : {}
    },
    "sort" :
    {
        "created_date" :
        {
             "order" : "asc"
        }
    }
}'

