---
title: 'Interim Report'
author: 'Mark Nemec'
abstract: ''
---

# Introduction

In recent years, there has been an **explosion** in cloud computation software. Starting with Google publishing their paper on MapReduce, many new frameworks for distributed computation have emerged, most notably Hadoop for batch processing and Storm for processing data streams.

Commercial companies and researchers have been able to utilise these frameworks and create distributed systems which can accomplish things that would not have been possible to achieve on a single computer. This has mostly been allowed by the low price of commodity hardware. While the price of such systems is perhaps lower than price of a supercomputer with equal power there are certain limitations.

Firstly, the nodes of a cluster need to communicate through a network. This limits the speed of communication between processes that live on different nodes.

Secondly, distributed systems waste resources due to data replication which enhances reliability and possibly performance. However, with this comes the problem of consistency.

Lastly, to run a distributed computation on commodity hardware one would usually need a server farm or to rent out instances on cloud computing services such as Amazon EC2 or Rackspace. This might not be ideal for some use cases which require a heightened level of security and would prefer full control over their system.

The main idea of these frameworks is to split the work that needs to be carried out and distribute it across multiple nodes in the cluster. The main idea of this project is to apply these ideas not in the context of clusters but in context of multicore CPUs.

# Description

# Done so far

# Remains to be done

# Timeline

# Conclusion
