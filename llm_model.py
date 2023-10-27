import os
from flask import Flask, render_template, request, redirect, url_for, session
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.chat_models import ChatOpenAI

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from pymongo import MongoClient

# Your MongoDB connection information
mongo_uri = "mongodb://localhost:27017/"
database_name = "recommendation_system"
collection_name = "users_survey_data"

# Create a MongoClient
client = MongoClient(mongo_uri)

# Connect to the database and collection
db = client[database_name]
collection = db[collection_name]

def get_course_name(user_email):
  # Define a new Pydantic model with field descriptions and tailored for Twitter.
  class CourseUser(BaseModel):
    course: str = Field(description="Which Course user will take from this four: 1.Software Engineering 2.Databases and Search 3.Algorithms and Computers 4.Artificial Intelligence  Give any one")

  # Instantiate the parser with the new model.
  parser = PydanticOutputParser(pydantic_object=CourseUser)

  # Update the prompt to match the new query and desired format.
  prompt = ChatPromptTemplate(
     messages=[
       HumanMessagePromptTemplate.from_template(
         "answer the users question as best as possible.\n{format_instructions}\n{question}"
       )
     ],
     input_variables=["question"],
     partial_variables={
       "format_instructions": parser.get_format_instructions(),
     },
  )

  chat_model = ChatOpenAI(
     model="gpt-3.5-turbo",
     openai_api_key="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",
     max_tokens=1000
  )

  #user_email = "test5@gmail.com"  # Replace with the user's email
  #user_email= session["email"]


  # Query the MongoDB collection to get user data
  user_data = collection.find_one({"user_email": user_email})
  if user_data:
    # You can access the user's survey data like this:
    initialInterest = user_data.get("initialInterest", "")
    techChallenges = user_data.get("techChallenges", "")
    proudProject = user_data.get("proudProject", "")
    aiInterest = user_data.get("aiInterest", "")
    dbInterest = user_data.get("dbInterest", "")
    seInterest = user_data.get("seInterest", "")
    algoInterest = user_data.get("algoInterest", "")
    longTermGoals = user_data.get("longTermGoals", "")
    # Get the user input
    # user_input = input("Enter your question: ")
    user_input = f"""
                    What initially drew you to study computer science?
                    Answer: {initialInterest}
                    What kind of technical challenges excite you the most?
                    Answer: {techChallenges}
                    Describe a project you've worked on that you're particularly proud of and would like to do more of.
                    Answer: {proudProject}
                    What are your thoughts on the field of Artificial Intelligence? Does the field interest you? If so, what interests you about it and what do you think we could achieve with AI?
                    Answer: {aiInterest}
                    How important do you think data management is in today's world? Are you interested in databases or search algorithms? How can you see yourself working with data?
                    Answer: {dbInterest}
                    Do you enjoy working on larger projects as part of a team? Are you interested in the software development lifecycle? Do you like being handed specific tasks, and achieve results frequently?
                    Answer: {seInterest}
                    Do you find joy in problem-solving or optimizing for performance? Are you interested in the theoretical aspects of computing? Do you like working in detail for optimization or on a higher level for visible results?
                    Answer: {algoInterest}
                    Long-term Career Goals and Interests?
                    Answer: {longTermGoals}
                    """

    # Generate the input using the updated prompt.
    _input = prompt.format_prompt(question=user_input)

    # I have added a try and except block here to handle errors from the OpenAI API.
    try:
        output = chat_model(_input.to_messages())
        parsed = parser.parse(output.content)

        print(output.content)
        print(parsed)
        print(type(parsed))
        parsed = str(parsed)
        course_name = parsed.split("=")[1].strip()  # Remove leading/trailing spaces
        course_name = course_name.replace("'", "")

        return course_name

    except Exception as e:
        print("An error occurred when calling the OpenAI API:", e)
        return "Error"
#get_course_name()