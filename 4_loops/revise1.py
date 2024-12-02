
# data=        {
#             "type": "Derivatives",
#             "holdings": [
#                 {"instrument": "Options", "details": {"type": "Call", "strike_price": 1500}}
#             ]
#         }

# # print(data.get('holdings')[0].get('details').get('underlying')) #None or Goog

# #truthy value or falsy value
# #falsy values None,0,"",[],False,{}
# if data.get('holdings')[0].get('details').get('underlying'):
#     print(data.get('holdings')[0].get('details').get('underlying'))
# else:
#     print('goog does not exisit')




