#
# # https://rasa.com/docs/rasa/custom-actions
#
from typing import Any, Text, Dict, List, Union
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from database import DataValue
from rasa_sdk.forms import FormAction
#
# class HealthForm(FormAction):
#
#     def name(self):
#         return "health_form"
#
#     @staticmethod
#     def required_slots(tracker):
#         if tracker.get_slot("confirm_exercise") == True:
#             return ["confirm_exercise", "exercise", "sleep", "diet", "stress", "goal"]
#         else:
#             return ["confirm_exercise", "sleep", "diet", "stress", "goal"]
#
#     # once all the slots are filed then we will execute this method
#     def submit(
#         self,
#         dispatcher: "CollectingDispatcher",
#         tracker: "Tracker",
#         domain: Dict[Text,Any],
#     ) -> List[Dict]:
#         return []
#     # if you do not define slot mapping then slots will be filled only by entities with the same name as the lots picked up by the user unputs
#     # so ths method tell rasa how to extract slot values form user responses
#     def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
#         return {
#             "confirm_exercise":[
#                 self.from_intent(intent="affirm", value=True),
#                 self.from_intent(intent="deny", value=False),
#                 self.from_intent(intent="inform", value=True),
#             ],
#             "sleep": [
#                 self.from_entity(entity="sleep"),
#                 self.from_intent(intent="deny",value="None"),
#             ],
#             "diet":[
#                 self.from_text(intent="inform"),
#                 self.from_text(intent="affirm"),
#                 self.from_text(intent="deny"),
#             ],
#             "goal":[
#                 self.from_text(intent="inform"),
#             ]
#         }

class ActionCheck(Action):
   def name(self) -> Text:
      return "action_check_detail"

   # @staticmethod
   # def required_slots(tracker):
   #     return "sure"
   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       email_info = tracker.get_slot('email')
       event = tracker.get_slot('category')
       place = tracker.get_slot('city')
       name = tracker.get_slot('name')
       date = tracker.get_slot('date')
       price = tracker.get_slot('price')
       allow = tracker.get_slot('sure')
       print(allow)
       res = DataValue(name, email_info, date, event, place, price, allow)
       print(res)
       # if res == 1 :
       #     dispatcher.utter_message(text="Thank You :) , Our support team will get in touch with you soon.")
       # else:
       #     pass
       # if res != None:
       #     dispatcher.utter_message(text="Your account is registered")
       # else:
       #     dispatcher.utter_message(text="This account is not registered with us.")
       return []

import requests
class ApiCheck(FormAction):

   def name(self) -> Text:
      return "action_check_api"

   @staticmethod
   def required_slots(tracker):
       if tracker.get_slot("filter") == "True":
           return ["filter","name","email","event","date","category","city","price"]
       if tracker.get_slot("ext") == True:
           # print("ok")
           return ["filter""name","email","event","date","category","city","price","ext"]
       else:
           return ["name","email","event","date","category","city","price"]


   def validate_price(
           self,
           value: Text,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any],
   ) -> Dict[Text, Any]:
       city = tracker.get_slot('city').lower()
       info = tracker.get_slot('category')
       price = tracker.get_slot('price')
       print(price)
       amt1=[]
       try:
           int(price)
           x=True
       except:
           x = False

       if x==False:
           for i in price:
               if i == 'k':
                   break
               amt1.append(i)
           price = int("".join(amt1)) * 1000
       api = 'http://13.127.226.85:10041/eventtow/search-service/global?q={}&start=0&maxResults=50'.format(info)
       current = requests.get(api).json()
       prod = current['products']
       place = []
       for i in range(len(prod)):
           if prod[i]['address'] == None:
               pass
           elif ((prod[i]['address']['city']).lower() == city) & (
                   int(prod[i]['price']) <= (int(price) if (int(price) != 0) else int(prod[i]['price']))):
               place.append(prod[i])
       prod = place
       if len(prod) == 0:
           dispatcher.utter_message("Sorry, I was unable to find any {} category vendor in the city {}\nTry increasing your budget".format(info,city))
           return {"price":None}
       else:
           return {"price":value}
       # try:
       #     int(value)
       #     return {"price":value}
       # except:
       #     print("not ok")
       #     dispatcher.utter_message("Please enter the price again , I'll try to understand it this time")




   def submit(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> list:
       global x
       info = tracker.get_slot('category')
       city = tracker.get_slot('city').lower()
       price = tracker.get_slot('price')
       filter = tracker.get_slot('filter')
       all = tracker.get_slot('ext')
       print(all)
       print(filter)
       # price_check = tracker.get_slot('price_check')
       print(price)
       # print(price_check)
       api= 'http://13.127.226.85:10041/eventtow/search-service/global?q={}&start=0&maxResults=50'.format(info)
       current= requests.get(api).json()
       prod = current['products']
       med=[]
       print(len(prod))
       print(prod[0]['price'])
       print(tracker.get_slot('email'))
       print(tracker.get_slot('date'))
       print(tracker.get_slot('name'))
       place =[]
       amt=[]
       if all != None:
           print("ok")
       try:
           int(price)
           for i in range(len(prod)):
               if prod[i]['address'] == None:
                   pass
               elif ((prod[i]['address']['city']).lower() == city) & (
                       int(prod[i]['price']) <= (int(price) if (int(price) != 0) else int(prod[i]['price']))):
                   place.append(prod[i])

       except:
           amt1=[]
           for i in price:
               amt.append(i)

           for i in range(len(amt) - 1):
               if ((amt[i] == 'k') & (amt[i + 1] == '+')):
                   x = True
               else:
                   x = False
           for i in price:
               if i == 'k':
                   break
               amt1.append(i)
           price = int("".join(amt1)) * 1000
           if (x == True):
               for i in range(len(prod)):
                   if prod[i]['address'] == None:
                       pass
                   elif ((prod[i]['address']['city']).lower() == city) & (
                           int(prod[i]['price']) >= (int(price) if (int(price) != 0) else int(prod[i]['price']))):
                       place.append(prod[i])
           elif (x ==False):
               for i in range(len(prod)):
                   if prod[i]['address'] == None:
                       pass
                   elif ((prod[i]['address']['city']).lower() == city) & (
                           int(prod[i]['price']) <= (int(price) if (int(price) != 0) else int(prod[i]['price']))):
                       place.append(prod[i])


       prod = place
       print(len(prod))
       res=[]
       for i in range(len(prod)):
           det = prod[i]['productName']
           det2= prod[i]['price']
           resp = """Vendor_name -> {} \nPrice_Of_Service -> {}""".format(det,det2)
           res.append(resp)

       # final =[]
       var = []
       buttons = []
       buttons.append({"title":'Yes',"payload":'Yes'})
       buttons.append({"title": 'No', "payload": 'No'})
       print(buttons)
       if len(res) > 0:
           if ((filter != None) & (all == None)):
               if len(res) >= 5:
                   res = res[:5]
                   message = "These are the best 5 search results for {} in {}".format(info, city)
               else:
                   message = "These are one of the best search results for {} in {}".format(info, city)
           else:
               message = "Here are all the search results for {} in {}".format(info, city)
           for i in range(len(res)):
               var.append(res[i])

           def listToString(s):
               string = " " + "\n"
               return (string.join(s))


           dispatcher.utter_message(message +"\n"+ listToString(var))
           dispatcher.utter_message(text="Were you satisfied with these results?",buttons=buttons)
       else:
           dispatcher.utter_message("Sorry, I was unable to find any {} category vendor in the city {}\nTry increasing your budget".format(info,city))
           return [SlotSet("price", None)]

       return [SlotSet("ext", None)]

   def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
       return {
           "sure":[
               self.from_intent(intent="ado", value=True),
               self.from_intent(intent="adont", value=False)
           ],
           "name":[
               self.from_entity(entity="name", intent=["name_info"]),
               self.from_intent(intent=["out_of_scope","deny","nlu_fallback"], value="customer")
           ],
           "date":[
               self.from_entity(entity="date", intent=["date_info"]),
               self.from_text(intent="date_format")
           ],
           "email":[
               self.from_entity(entity="email", intent=["email_info"])
           ],
           "price": [
               self.from_entity(entity="price", intent=["price_ext"]),
               self.from_intent(intent=["deny","inform","thankyou"], value="0")
               # self.from_text(intent="price_info")
           ],
           "filter": [
               self.from_intent(intent=["filter+search_category","search_category"], value="True")
           ],
           "ext": [
               self.from_intent(intent="everything", value=True)
           ]
        }