from dg.settings import COMPLETION_INDEX, FACET_INDEX

SETTINGS = {
            "analysis":{
               "filter":{
                  "name_ngrams":{
                     "side":"front",
                     "max_gram":20,
                     "min_gram":2,
                     "type":"edgeNGram"
                  }
               },
               "analyzer":{
                  "full_name":{
#                     "filter":[
#                        "standard",
#                        "lowercase",
#                        "asciifolding"
#                     ],
                     "type":"custom",
                     "tokenizer":"keyword"
                  },
                  "partial_name":{
                     "filter":[
                        "standard",
                        "lowercase",
                        "asciifolding",
                        "name_ngrams"
                     ],
                     "type":"custom",
                     "tokenizer":"standard"
                  }
               }
            }
         }


FACET_MAPPING = {
         FACET_INDEX :{
                 "properties":{
                               "subcategory" : {
                                            "fields":{
                                                      "subcategory":{
                                                                     "type":"string",
                                                                     "analyzer":"keyword"
                                                                 },
                                                      "partial":{
                                                                 "search_analyzer":"full_name",
                                                                 "index_analyzer":"partial_name",
                                                                 "type":"string"
                                                                 }
                                                      },
                                            "type":"multi_field"
                                            },
                               "category" : {
                                            "fields":{
                                                      "category":{
                                                                 "type":"string",
                                                                 "analyzer":"keyword"
                                                                 },
                                                      "partial":{
                                                                 "search_analyzer":"full_name",
                                                                 "index_analyzer":"partial_name",
                                                                 "type":"string"
                                                                 }
                                                      },
                                            "type":"multi_field"
                                            },
                               "topic" : {
                                            "fields":{
                                                      "topic":{
                                                                 "type":"string",
                                                                 "analyzer":"keyword"
                                                                 },
                                                      "partial":{
                                                                 "search_analyzer":"full_name",
                                                                 "index_analyzer":"partial_name",
                                                                 "type":"string"
                                                                 }
                                                      },
                                            "type":"multi_field"
                                            },
                               "subject" : {
                                            "fields":{
                                                      "subject":{
                                                                 "type":"string",
                                                                 "analyzer":"keyword"
                                                                 },
                                                      "partial":{
                                                                 "search_analyzer":"full_name",
                                                                 "index_analyzer":"partial_name",
                                                                 "type":"string"
                                                                 }
                                                      },
                                            "type":"multi_field"
                                            },
                                     
                               "language" : {
                                            "fields":{
                                                      "language":{
                                                                 "type":"string",
                                                                 "analyzer":"keyword"
                                                                 },
                                                      "partial":{
                                                                 "search_analyzer":"full_name",
                                                                 "index_analyzer":"partial_name",
                                                                 "type":"string"
                                                                 }
                                                      },
                                            "type":"multi_field"
                                            },
                               "partner" : {
                                            "fields":{
                                                      "partner":{
                                                                 "type":"string",
                                                                 "analyzer":"keyword"
                                                                 },
                                                      "partial":{
                                                                 "search_analyzer":"full_name",
                                                                 "index_analyzer":"partial_name",
                                                                 "type":"string"
                                                                 }
                                                      },
                                            "type":"multi_field"
                                            },
                               "state" : {
                                          "fields":{
                                                    "state":{
                                                             "type":"string",
                                                             "analyzer":"keyword"
                                                             },
                                                    "partial":{
                                                               "search_analyzer":"full_name",
                                                                "index_analyzer":"partial_name",
                                                                "type":"string"
                                                                }
                                                    },
                                            "type":"multi_field"
                                            },
                               "videos" : {
                                            "type" : "nested",
                                            },
                   }
           }
        }

COMPLETION_MAPPING = {
                      COMPLETION_INDEX:{
                                    "properties":{
                                                  "searchTerm":{
                                                                "fields":{
                                                                          "searchTerm":{
                                                                                        "type":"string",
                                                                                        "analyzer":"full_name"
                                                                                        },
                                                                          "partial":{
                                                                                     "search_analyzer":"full_name",
                                                                                     "index_analyzer":"partial_name",
                                                                                     "type":"string"
                                                                                     }
                                                                          },
                                                                "type":"multi_field"
                                                                }
                                                  }
                                    }
                      }