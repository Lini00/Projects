This project is a simple question answering system based on inverse document frequency.

This question answering system will perform two tasks: document retrieval and passage retrieval. This system will have access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval will first identify which document(s) are most relevant to the query. Once the top documents are found, the top document(s) will be subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.

To find the most relevant documents, This system uses tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. Once the most relevant documents sre found, there many possible metrics for scoring passages, this system uses a combination of inverse document frequency and a query term density measure 
