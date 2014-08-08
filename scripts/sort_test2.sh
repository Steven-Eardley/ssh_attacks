curl -XPOST 'localhost:9200/ssh_attacks/ssh_entry/_search' -d '

{
    "query":
    {
        "bool":
        {
            "must":
            [{
                "term": 
                {"attack_name": "admin"}
            }]
        }
    }
}'

