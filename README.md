search-ctl
==========

Little python script to search an ElasticSearch index from the command line. Utterly useless


    curl -XDELETE 'http://localhost:9200/code/'


    curl -XPUT 'localhost:9200/code' -d '{
     "settings" : {
     },
     "mappings" : {
         "source_file" : {
             "properties" : {
                 "file_name" : {
                     "type" : "string",
                     "analyzer" : "standard"
                 },
                 "path" : {
                     "type" : "string",
                     "analyzer" : "standard"
                 },
                 "language" : {
                     "type" : "string",
                     "analyzer" : "standard"
                 },
                 "source_code" : {
                     "type" : "string",
                     "analyzer" : "standard"
                 }
             }
         }
     }
    }'

    curl -XGET http://localhost:9200/code/_search\?pretty -d '{
         "query" : {
             "term" : { "language": "py" }
         }
     }'

