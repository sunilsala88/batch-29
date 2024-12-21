
with open('data.txt','r') as f1:
    data=f1.read()
data_list=data.split('\n')
print(data_list)



# for num in data_list:
#         s=int(num)**2
#         print(s)
# with open('output.txt','w') as f2:
    # f2.write(s)