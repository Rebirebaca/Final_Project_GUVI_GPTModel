# Deployment GUVI GPT Model using Hugging Face

## Introduction:
The task is to deploy a fine-tuned GPT model, trained specifically on GUVI’s company data, using Hugging Face services. The application includes a Streamlit-based chatbot interface, offering secure user authentication with encrypted passwords to ensure privacy. User data is stored in TiDB Cloud for robust and scalable data management.User are required to create a scalable and secure web application using Streamlit or Gradio, making the model accessible to users over the internet.

## Domain: AIOPS

## Technology and Skills Takeaway
Deep Learning
Transformers
Hugging face models
LLM
bcrypt
TIDB Cloud Database
Streamlit

## Objectives
To deploy a pre-trained or Fine tuned GPT model using HUGGING FACE SPACES, making it accessible through a web application built with Streamlit or Gradio for user interaction.

## Business Use Cases
### Customer Support Automation :
Integrate the model with GUVI’s customer support system to automate responses to frequently asked questions.

### Content Generation for Marketing :
Generate marketing content like blog posts, social media updates, and email newsletters tailored to GUVI’s audience.

### Educational Assistance for Students :
Implement the model as a virtual teaching assistant within GUVI’s educational platform.

### Internal Knowledge Base :
Develop a tool for GUVI employees to access company-related information and resources quickly.

### Training and Onboarding :
Assist in the training and onboarding process of new employees by providing instant access to training materials and answering common questions.


## Project Workflow
### Data Preperation
#### Data Collection:
Gather text data from various sources within GUVI, such as website content, user queries, social media, blog posts, and training materials.
#### Data Cleaning: 
Clean and preprocess the text data, ensuring it is in a format suitable for training.
#### Tokenization: 
Use the GPT-2 tokenizer to convert the text data into tokens.

### Fine-Tuning Model
#### Training: 
Fine-tune the GPT-2 model using the Hugging Face Transformers library on the prepared dataset.
#### Monitoring: 
Monitor the training process to prevent overfitting and ensure the model generalizes well to new data.

### Infrastructure Setup
#### Deployment using Hugging Face Spaces: 
Deploy the fine-tuned model using Hugging Face Spaces.
#### Environment Configuration: 
Set up the required environment and install necessary packages.

### Web Application Development
#### Streamlit: 
Develop the web application interface using Streamlit.

### User Authentication
#### System Authentication: 
Create login, signup, and password reset functionalities using bcrypt for password encryption.
#### Storage of user data : 
Securely store user data and login details.

### Requirements
Python 3.8+ PyTorch Transformers (Hugging Face) Streamlit Accelarate-u Other dependencies specified in requirements.txt

## Deployment
To deploy this project run just click the below link
https://huggingface.co/spaces/Rebaca/Guvi_GPT

## Disclaimer
This application is designed to provide information to demonstration of a language model and is not affiliated with GUVI.This model may not always be accurate or appropriate. Use it at your own discretion.

## Reference
### Hugging Face Spaces Documentation: 
https://huggingface.co/docs/hub/en/spaces-overview
### Streamlit Documentation: 
https://docs.streamlit.io/
### TIDB Cloud Documentaion: 
https://docs.pingcap.com/tidbcloud/





