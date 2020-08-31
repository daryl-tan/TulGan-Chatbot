# TulGan Chatbot
This project was created by Tan RongJun Daryl and Teo Jun Hao Bryan as part of the CP2106 - Independent Software Development Project (Orbital) module in NUS. 

The chatbot can be accessed at https://tulgan.herokuapp.com/, and a video explaining this project can be viewed at https://youtu.be/Gt6pCRqgf2g/. 

## Motivation
We have all been there before, scouring the various NUS websites for information in an attempt to make an informed decision before choosing a major which influences our next stage of life. Despite our best efforts, finding information regarding the various majors was a hassle. 

## Project Vision
Our vision is to create a chatbot integrated into the NUS website that provides instant, intelligent and contextualized answers to queries from freshmen entering NUS Computing. The chatbot will provide robust reasoning and intelligent responses. Getting information would be as simple as asking a friend/ senior in NUS, with the chatbot providing objective information instantly.  

## Aim
We aim to provide a chatbot that serves as a gateway to relevant information, that centers around freshmen that are entering NUS Computing, convenience and accuracy. We aim to ensure good user experience by understanding the needs of our users and providing an intuitive platform for them to ask questions. 

## Features and Deliverables
The chatbot provides a chat interface for users to ask questions and the chatbot will provide answers from a database. 

1. Quick and accurate answers
    1. The chatbot will provide answers to user queries immediately with a low rate of error. 
    
2. Gather feedback on answers provided
    1. Allows us to identify what information is lacking from the NUS website, thereby allowing us to see information gaps present in the NUS website
    2. It will be used to retrain the code to further improve the accuracy of the answers provided. 
    3. It will be used to quantify the chatbot’s error rate.   
    
3. Contextualized answers
    1. Asking a generic question will prompt the chatbot to ask the user for a more specific question. e.g. if a user asks the chatbot for information regarding the NUS curriculum, the chatbot will respond by asking the user for what faculty he is referring to.  
    
4. Analysis of user queries
    1. The chatbot will log down user queries which allow for unanswered queries to be added to the FAQ database. 
    2. The insights gained can also be relayed to SoC staff to be addressed during open house. 
    
5. Automated testing 
    1. Automation has enabled us to test our model ability to provide contextualized responses, provide accurate answers regardless of minor spelling errors or queries that the model was not trained for and the chatbot web interface.
    2. The time gain from conducting manual exploratory tests would enable us to increase the extensibility and coverage of our test.
    
6. Type annotations and assertions 
    1. In view of the language we used, Python which is a dynamic typed language, we have embedded type annotations extensively into our codes. This enables us to add type hints into our variables.
    2. In addition, we have incorporated assert statements into our codes to help us detect potential problems early on thus, minimizing side-effects when our model is deployed.
    
7. RESTful API responses
    1. APIs enable various platforms (Telegram Bot) to interact with our model. It forms the foundation and removes the need for rebuilding the whole TensorFlow model.
    2. A new interface can be easily developed by making an API call either for a response from the bot or analysis of the database of queries. 
    
## Workflow
When the user types a query into the chatbot web interface, a POST request with the query is sent to the API framework. The query will first be processed before it is passed into the model. The model will return the appropriate tag with the highest probability. 

The tag and the unprocessed user’s query is first stored into our SQL database together with the date stamp. The tag is then used to obtain the relevant responses from the JSON file before it is returned as a reply to the user.

When the user feedbacks the relevance of the reply, another POST request is made to the backend to update the relevancy of the reply from the model which has been set to null as default.

When a POST request is sent to the backend together with an email address, the analytical pipeline is triggered. The pipeline will first pull the stored queries from the SQL database which will be read into a data frame. The data frame is processed to remove irrelevant replies, grouped and the top 5 query categories are plotted into a bar chart. The bar chart and the CSV file of the data frame are then emailed to the email address sent from the POST request.

## Deep Learning Process 
The Tensorflow model was developed using a neural network with 4 hidden layers. The neural network will take in a bag of words and return a category (tag) that has the highest probability. The model was then trained with a JSON file that is made of self-written messages that a user is likely to query and mapped to a bunch of relevant responses.

The queries stored in the SQL database will be pulled and added into our JSON file which will be used to retrain the model. Queries with irrelevant responses will be reviewed and used to expand the scope of our chatbot. As a result, over time the accuracy of the model’s responses will increase as the number of queries increases. 

## Lessons Learnt
1. Leverage on Git for a collaborative coding project. It allows us to work separately on different aspects of the same project and merge our codes seamlessly.
2. Leverage on automated testing for greater extensibility and coverage. It enables us to focus less on manual exploratory tests. 
3. Importance of user experience when developing a product. This is crucial in ensuring the success and adoption of the product.
4. Leverage on RESTful API for project extensibility. It allows us and other potential developers to focus on developing the interface without the need to re-create the Tensorflow model.
5. Importance of setting aims and goals at the start of the project to ensure that we are always on the right path.
6. Importance of understanding the needs of the target audience through conducting surveys. This allows us to create an application with the right features for the target audience.

## Future Extensions
1. Include other faculties in NUS.
2. Redirect to a live chat within the web-based chat for urgent unresolved queries.
3. Expand the chatbot platforms (e.g. Facebook Messengers, Telegram, etc)
4. Get feedback from NUS Staff on features and usability


