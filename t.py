import random
def extends_accounts(accounts,videocount):
    # Your lists
    videos = [1, 2, 3, 4, 5]  # Replace with your list1
    accounts = ['A', 'B', 'C']  # Replace with your list2
    videocount=len(videos)
    n = videocount
    m = len(accounts)
    ratio = n / m

    extended_list2 = []

    for _ in range(n):
        if ratio.is_integer():
            # If n/m is an integer, repeat elements from list2
            extended_list2.append(accounts[_ % m])
        else:
            # If n/m is not an integer, choose a random element from list2
            extended_list2.append(random.choice(accounts))    
    return extended_list2
print(extends_accounts(1,2))
videos = [1, 2, 3, 4, 5]  # Replace with your list1
accounts = ['A', 'B', 'C']  # Replace with your list2
print([random.choice(accounts)  for x in range(0,len(videos))])