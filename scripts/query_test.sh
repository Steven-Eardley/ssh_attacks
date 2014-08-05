curl -XPOST "localhost:9200/ssh_attacks/ssh_entry/_search?pretty" -d'
{
"size" : 0,
"aggregations" :
    {
    "name_count" :
         {
         "terms" :
            {
            "field" : "attack_name"
            }
        }
   }
}'
