#IP Overlap Script.

This script «flattens» the overlapping IP ranges
producing the non-overlapping ranges.

For the following input:

```csv
1.1.1.1,10.10.10.10,US,T-Mobile
2.2.2.2,3.3.3.3,US,Sprint
5.5.5.5,8.8.8.8,AU,Telstra
6.6.6.6,7.7.7.7,AU,voda AU
```

the script will produce the following output:

```csv
1.1.1.1,2.2.2.1,US,T-Mobile
2.2.2.2,3.3.3.3,US,Sprint
3.3.3.4,5.5.5.4,US,T-Mobile
5.5.5.5,6.6.6.5,AU,Telstra
6.6.6.6,7.7.7.7,AU,voda AU
7.7.7.8,8.8.8.8,AU,Telstra
8.8.8.9,10.10.10.10,US,T-Mobile
```
