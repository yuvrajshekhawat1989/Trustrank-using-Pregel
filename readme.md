# Implementing Trustrank using Pregel framework

## How to run
1. Download the zip file it must contain files *"Iron_dealers_data.csv","bad.csv","pregel.py","pregel_trustrank.py"*.
2. Run file *"pregel_trustrank.py"* using command *"python3 pregel_trustrank.py"*.
3. A new file *"DealerTrustScores.txt"* will be created. It will have scores for all nodes in descending order.

## Problem Statement
In a business ecosystem, there are numerous dealers who frequently buy and sell goods to each other. Each dealer is identified by a unique ID associated with it. To track the trustworthiness of these dealers, we are provided with a CSV file containing transaction details in the format of `(seller ID, buyer ID, transaction amount)`.

We are also provided with a list of bad dealers who have been flagged for exhibiting suspicious behavior. These dealers may have indulged in fraudulent activities or have a history of unreliable transactions.

We aim to identify the bad dealers who may have a negative impact on the overall trustworthiness of the ecosystem. For that, we propose to use the TrustRank algorithm to assign a bad trust score to all dealers. The more the bad score of a dealer is, the more likely he is fraud.

## Solution Overview
The TrustRank algorithm is well-suited for this problem, as it can effectively evaluate the trustworthiness of nodes in a graph-based model. In our case, the dealers can be represented as nodes in a graph, and the transactions between them can be represented as edges. The TrustRank algorithm can then be applied to this graph to assign trust scores to all the dealers.

We are using Pregel, a distributed computing framework, to implement the TrustRank algorithm. Pregel can handle large-scale graphs and can efficiently process the graph data in parallel. We can use Pregel to propagate the bad trust scores through the graph, starting from the bad dealers, and updating the trust scores of all other dealers in the ecosystem.

## Algorithm
We provide two algorithms for implementing Trustrank: one using the transition matrix and the other using the Pregel framework. Please refer to the LATEX report for the detailed algorithms.

## Dataset Description
- We have a total of 130,535 transactions, each containing the seller ID, buyer ID, and transaction value.
- There are 799 unique IDs, which means there are 799 dealers.
- Most of the transactions are between the same set of dealers, with only 5,358 transactions between different dealers.

## Results
- Most of the dealers have a trust score of 0.
- The bad dealers from the given set have higher trust scores.

For more detailed information and analysis of the results, please refer to the LATEX report.
