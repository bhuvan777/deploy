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
      return "action_check_email"

   def run(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
       info = tracker.get_slot('email')

       res = DataValue(info)
       if res != None:
           dispatcher.utter_message(text="Your account is registered")
       else:
           dispatcher.utter_message(text="This account is not registered with us.")
       return []

import requests
class ApiCheck(FormAction):

   def name(self) -> Text:
      return "action_check_api"

   @staticmethod
   def required_slots(tracker):
       if tracker.get_slot("filter") == "True":
           return ["filter","price","category","city"]
       if tracker.get_slot("ext") == True:
           # print("ok")
           return ["filter","price","category","city","ext"]
       else:
           return ["price","category","city"]

   def submit(self,
           dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> list:
       info = tracker.get_slot('category')
       city = tracker.get_slot('city')
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
       place =[]

       if all != None:
           print("ok")
       for i in range(len(prod)):
           if prod[i]['address'] == None :
               pass
           elif ((prod[i]['address']['city']).lower() == city) & (int(prod[i]['price']) <= (int(price) if (int(price) != 0) else int(prod[i]['price']))):
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
       buttons = []
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
               buttons.append(res[i])

           def listToString(s):
               string = " " + "\n"
               return (string.join(s))


           dispatcher.utter_message(message +"\n"+ listToString(buttons))
       else:
           dispatcher.utter_message("Sorry, I was unable to find any {} category vendor in the city {}\nTry increasing your budget".format(info,city))


       return [SlotSet("ext", None)]

   def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict[Text, Any]]]]:
       return {
           "price": [
               self.from_entity(entity="price", intent=["price_ext"]),
               self.from_intent(intent=["deny","inform","thankyou"], value="0"),
           ],
           "filter": [
               self.from_intent(intent=["filter+search_category","search_category"], value="True")
           ],
           "ext": [
               self.from_intent(intent="everything", value=True)
           ]
        }