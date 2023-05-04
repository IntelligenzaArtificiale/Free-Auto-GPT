from EdgeGPT import Chatbot, ConversationStyle
import asyncio

import requests
from langchain.llms.base import LLM
from typing import Optional, List, Mapping, Any
import pydantic
import os
from langchain import PromptTemplate, LLMChain
from time import sleep



class BingChat(LLM):
    
    history_data: Optional[List] = []
    cookiepath : Optional[str]
    chatbot : Optional[Chatbot] = None
    conversation_style : Optional[str] 
    conversation_style_on : Optional[ConversationStyle] = ConversationStyle.precise
    search_result : Optional[bool] = False
    
    @property
    def _llm_type(self) -> str:
        return "custom"
    
    def select_conversation(self, conversation_style: str):
        if conversation_style == "precise":
            self.conversation_style_on = ConversationStyle.precise
        elif conversation_style == "creative":
            self.conversation_style_on = ConversationStyle.creative
        elif conversation_style == "balaced":
            self.conversation_style_on = ConversationStyle.balanced
        else:
            raise ValueError("conversation_style must be precise, creative or balaced")
        self.conversation_style = conversation_style

    async def call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        #cookiepath is a must check
        if self.chatbot is None:
            if self.cookiepath is None:
                raise ValueError("Need a COOKIE , check https://github.com/acheong08/EdgeGPT/tree/master#getting-authentication-required for get your COOKIE AND SAVE")
            else:
                #if self.chatbot == None:
                self.chatbot = await Chatbot.create(cookie_path=self.cookiepath)
               
        if self.conversation_style is not None:
            self.conversation_style_on = self.select_conversation(self.conversation_style)
            
        response = await self.chatbot.ask(prompt=prompt, conversation_style=self.conversation_style, search_result=self.search_result)
        """
        this is a sample response. 
        {'type': 2, 'invocationId': '0', 
        'item': {'messages': [{'text': 'Hello, how are you?', 'author': 'user', 'from': {'id': '985157152860707', 'name': None}, 'createdAt': '2023-05-03T19:51:39.5491558+00:00', 'timestamp': '2023-05-03T19:51:39.5455787+00:00', 'locale': 'en-us', 'market': 'en-us', 'region': 'us', 'messageId': '87f90c57-b2ad-4b3a-b24f-99f633f5332f', 'requestId': '87f90c57-b2ad-4b3a-b24f-99f633f5332f', 'nlu': {'scoredClassification': {'classification': 'CHAT_GPT', 'score': None}, 'classificationRanking': [{'classification': 'CHAT_GPT', 'score': None}], 'qualifyingClassifications': None, 'ood': None, 'metaData': None, 'entities': None}, 'offense': 'None', 'feedback': {'tag': None, 'updatedOn': None, 'type': 'None'}, 'contentOrigin': 'cib', 'privacy': None, 'inputMethod': 'Keyboard'}, {'text': "Hello! I'm doing well, thank you. How can I assist you today?", 'author': 'bot', 'createdAt': '2023-05-03T19:51:41.5176164+00:00', 'timestamp': '2023-05-03T19:51:41.5176164+00:00', 'messageId': '1d013e71-408b-4031-a131-2f5c009fe938', 'requestId': '87f90c57-b2ad-4b3a-b24f-99f633f5332f', 'offense': 'None', 'adaptiveCards': [{'type': 'AdaptiveCard', 'version': '1.0', 'body': [{'type': 'TextBlock', 'text': "Hello! I'm doing well, thank you. How can I assist you today?\n", 'wrap': True}]}], 
        'sourceAttributions': [], 
        'feedback': {'tag': None, 'updatedOn': None, 'type': 'None'}, 
        'contentOrigin': 'DeepLeo', 
        'privacy': None, 
        'suggestedResponses': [{'text': 'What is the weather like today?', 'author': 'user', 'createdAt': '2023-05-03T19:51:42.7502696+00:00', 'timestamp': '2023-05-03T19:51:42.7502696+00:00', 'messageId': 'cd7a84d3-f9bc-47ff-9897-077b2de12e21', 'messageType': 'Suggestion', 'offense': 'Unknown', 'feedback': {'tag': None, 'updatedOn': None, 'type': 'None'}, 'contentOrigin': 'DeepLeo', 'privacy': None}, {'text': 'What is the latest news?', 'author': 'user', 'createdAt': '2023-05-03T19:51:42.7502739+00:00', 'timestamp': '2023-05-03T19:51:42.7502739+00:00', 'messageId': 'b611632a-9a8e-42de-86eb-8eb3b7b8ddbb', 'messageType': 'Suggestion', 'offense': 'Unknown', 'feedback': {'tag': None, 'updatedOn': None, 'type': 'None'}, 'contentOrigin': 'DeepLeo', 'privacy': None}, {'text': 'Tell me a joke.', 'author': 'user', 'createdAt': '2023-05-03T19:51:42.7502743+00:00', 'timestamp': '2023-05-03T19:51:42.7502743+00:00', 'messageId': '70232e45-d7e8-4d77-83fc-752b3cd3355c', 'messageType': 'Suggestion', 'offense': 'Unknown', 'feedback': {'tag': None, 'updatedOn': None, 'type': 'None'}, 'contentOrigin': 'DeepLeo', 'privacy': None}], 'spokenText': 'How can I assist you today?'}], 'firstNewMessageIndex': 1, 'defaultChatName': None, 'conversationId': '51D|BingProd|3E1274E188350D7BE273FFE95E02DD2984DAB52F95260300D0A2937162F98FDA', 'requestId': '87f90c57-b2ad-4b3a-b24f-99f633f5332f', 'conversationExpiryTime': '2023-05-04T01:51:42.8260286Z', 'shouldInitiateConversation': True, 'telemetry': {'metrics': None, 'startTime': '2023-05-03T19:51:39.5456555Z'}, 'throttling': {'maxNumUserMessagesInConversation': 20, 'numUserMessagesInConversation': 1}, 'result': {'value': 'Success', 'serviceVersion': '20230501.30'}}}
        """
        response_messages = response.get("item", {}).get("messages", [])
        response_text = response_messages[1].get("text", "")
        
        if response_text == "":
            # reset the chatbot and remake the call
            print("[DEBUGGER] Chatbot failed to respond. Resetting and trying again. [DEBUGGER]")
            sleep(10)
            self.chatbot = await Chatbot.create(cookie_path=self.cookiepath)
            sleep(2)
            response = await self.chatbot.ask(prompt=prompt)
            response_messages = response.get("item", {}).get("messages", [])
            response_text = response_messages[1].get("text", "")
        
        #add to history
        self.history_data.append({"prompt":prompt,"response":response_text})    
        
        return response_text
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        return asyncio.run(self.call(prompt=prompt))

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model": "BingCHAT", "cookiepath": self.cookiepath}



#llm = BingChat(cookiepath = "YOUR-COOKIE") #for start new chat
#llm = BingChat(cookiepath = "YOUR-COOKIE", conversation_style = "precise") #precise, creative or balaced
#llm = BingChat(cookiepath = "YOUR-COOKIE" , conversation_style = "precise" , search_result=True) #with web access

#print(llm("Hello, how are you?"))
#print(llm("what is AI?"))
#print(llm("Can you resume your previus answer?")) #now memory work well
