---
created: 2025-02-27T20:31
updated: 2025-02-27T21:02
---
# 시간복잡도
입력값과 문제를 해결하는 데 걸리는 시간과의 상관관계를 말한다.

## O(n^2)
```python
numbers = [1,2,3,2,1,3,1,4,2,1]
def find_most_frequent_numbers(numvers):
	for num in numbers:
		for compare_num in numbers:
			if num == compare_num:
				current_count += 1
	if current_count > max_count:
		max_count = current_count
		most_frequent = num
	return most_frquent, max_count
```

## O(n)
```python
numbers = [1,2,3,2,1,3,1,4,2,1]
def find_most_frequent_numbers(numbers):
	count_dict = {}
	for num in numbers:
		if num in count_dict:
			count_dict[num] += 1
		else:
			count_dict[num] = 1
	most_frequent = None
	max_count = 0

	for num, count in count_dict.item():
		if count > max_count:
			max_count = count
			most_frequent = num
	return most_frequent, max_count
	
```
