# Print-Similar
A small web service for printing similar words in the English language.

Two words w_1 and w_2 are considered similar if w_1 is a letter permutation of w_2 (e.g., "stressed" and "desserts"). 

## DB
A DB of the English dictionary should be provided.  
The service expects the DB (the txt file) to be in the local directory with the same name. 

## Web service API
The web service listen on port 8000 and support the following two HTTP endpoints:

### similar 
GET /api/v1/similar?word=stressed  
Returns all words in the dictionary that has the same permutation as the word "stressed".  
The word in the query should not be returned. 

The result format is a JSON object as follows:
```
{
    similar:[list,of,words,that,are,similar,to,provided,word]
}
```

#### Example
http://localhost:8000/api/v1/similar?word=apple
```
{"similar":["appel","pepla"]}
```

### stats 
GET /api/v1/stats  
Return general statistics about the program:
1. Total number of words in the dictionary
1. Total number of requests (not including "stats" requests)
1. Average time for request handling in nano seconds (not including "stats" requests)

The output is a JSON object structured as follows:
```
{
    totalWords:int
    totalRequests:int
    avgProcessingTimeNs:int
}
```

#### Example
http://localhost:8000/api/v1/stats
```
{"totalWords":351075,"totalRequests":9,"avgProcessingTimeNs":45239}
```
