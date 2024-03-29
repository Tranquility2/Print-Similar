# Print-Similar
A small web service for printing similar words in the English language.

Two words w_1 and w_2 are considered similar if w_1 is a letter permutation of w_2 (e.g., "stressed" and "desserts"). 

## How To Use
As Docker is used to simplify and ease the use of this web service, please make sure you have Docker installed:
https://docs.docker.com/install/linux/docker-ce/ubuntu/
### build
```sudo docker build -t print-similar .```
### run
```sudo docker run -p 8000:8000/tcp -it print-similar```

## DB
A DB of the English dictionary should be provided.  
The service expects the DB ("words_clean.txt" text file) to be in the local directory. 
### Algorithm
The data is stored in a simple dictionary structure where the key is the sorted permutation for a given word
and the value is a list of words can are sorted to the same base permutation, for example:  
```{'aelpp' : ["appl", "appel","pepla"]}```
In the app startup process we build this data word by word from the given words file.  
Method to find similar words:  
1. sort the given input
1. get the correlating values 
1. remove the input word from the values
1. return the remaining values 

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

## Overview
![Overview](docs/diag.png)

## Notes/TODOs
1. The input dictionary text file in not validated/sanitized
1. Requests without a result will just return ```{"similar":[]}``` and not an error code
(please make sure that the file only contains one word per line format)
1. Flask-Cache should be introduced to enable caching (https://pythonhosted.org/Flask-Cache/)
