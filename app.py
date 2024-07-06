# Import libraries:
import streamlit as st
import mysql.connector
import bcrypt
import datetime
import re
import pytz
import time
from transformers import GPT2LMHeadModel, GPT2Tokenizer     #Import transformers library for GPT-2 model
import torch

#streamlit part:
st.set_page_config(page_title="GUVI GPT Model LLM PROJECT", page_icon="chatgpt.png")

#To connect TiDB Cloud database:
mydb = mysql.connector.connect(
  host = "gateway01.us-east-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "2JDPogwqN11wk2n.root",
  password = "C3cQvJFFlFpzPRrR",
  database = "test")
mycursor = mydb.cursor(buffered=True)

# Create 'test' database:
mycursor.execute("CREATE DATABASE IF NOT EXISTS test")
mycursor.execute('USE test')

# Create 'users_info' table if it does not exist:
mycursor.execute('''CREATE TABLE IF NOT EXISTS user_info(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(155) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL ,
                registered_date TIMESTAMP,
                last_login TIMESTAMP); ''')


#Check if username data in the database:
def username_data(username):
    mycursor.execute("SELECT * FROM user_info WHERE username = %s", (username,))
    return mycursor.fetchone() is not None

#Check if email data in the database;
def email_data(email):
    mycursor.execute("SELECT * FROM user_info WHERE email = %s", (email,))
    return mycursor.fetchone() is not None

#To validate email format using regular expressions:
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

#Create a new user in the database:
def create_user(username, password, email):
    if username_data(username):
        return 'username_data'
    
    if email_data(email):
        return 'email_data'
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    registered_date = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    # Insert user data into 'user_info' table
    mycursor.execute(
        "INSERT INTO user_info (username, password, email, registered_date) VALUES (%s, %s, %s, %s)",
        (username, hashed_password, email, registered_date)
    )
    mydb.commit()
    return 'success'

#To verify user details:
def to_verify_user(username, password):
    mycursor.execute("SELECT password FROM user_info WHERE username = %s", (username,))
    record = mycursor.fetchone()
    if record and bcrypt.checkpw(password.encode('utf-8'), record[0].encode('utf-8')):
        mycursor.execute("UPDATE user_info SET last_login = %s WHERE username = %s", (datetime.datetime.now(pytz.timezone('Asia/Kolkata')), username))
        mydb.commit()
        return True
    return False

#Reset user password:
def to_reset_password(username, new_password):
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    mycursor.execute(
        "UPDATE user_info SET password = %s WHERE username = %s",
        (hashed_password, username))
    mydb.commit()


#Load the fine-tuned model and tokenizer:
model_name_or_path =  "./finetuned_model271230"
model = GPT2LMHeadModel.from_pretrained(model_name_or_path)
token_name_or_path = "./finetuned_model271230"
tokenizer = GPT2Tokenizer.from_pretrained(token_name_or_path)


#Set the pad_token to eos_token if it's not already set
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

#Move the model to GPU if available:
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)


#Define the text generation function:
def generate_text(model, tokenizer, seed_text, max_length=100, temperature=1.0, num_return_sequences=1):
    
    #Tokenize the input text with padding:
    inputs = tokenizer(seed_text, return_tensors='pt', padding=True, truncation=True)

    input_ids = inputs['input_ids'].to(device)
    attention_mask = inputs['attention_mask'].to(device)

    #Generate text:
    with torch.no_grad():
        output = model.generate(
            input_ids,
            attention_mask=attention_mask,
            max_length=max_length,
            temperature=temperature,
            num_return_sequences=num_return_sequences,
            do_sample=True,
            top_k=50,
            top_p=0.50,
            pad_token_id=tokenizer.eos_token_id  # Ensure padding token is set to eos_token_id
        )

    #Decode the generated text:
    generated_texts = []
    for i in range(num_return_sequences):
        generated_text = tokenizer.decode(output[i], skip_special_tokens=True)
        generated_texts.append(generated_text)

    return generated_texts

#Session state management:
if 'sign_up_successful' not in st.session_state:
    st.session_state.sign_up_successful = False
if 'login_successful' not in st.session_state:
    st.session_state.login_successful = False
if 'reset_password' not in st.session_state:
    st.session_state.reset_password = False
if 'username' not in st.session_state:
    st.session_state.username = ''
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'login'

def home_page():
    st.title(f"Welcome to GUVI-GPT, {st.session_state.username}!")
    st.write("Thank you for logging in.")
    st.info("Disclaimer: This application is designed to provide information to demonstration of a language model and is not affiliated with GUVI.This model may not always be accurate or appropriate. Use it at your own discretion.")

    # Text generation section
    st.subheader("Generate Text")
    seed_text = st.text_input("Enter the text:")
    max_length = st.slider("Max length", min_value=10, max_value=500, value=100)
    #temperature = st.slider("Temperature", min_value=0.1, max_value=2.0, value=1.0)
    #num_return_sequences = st.slider("Number of sequences", min_value=1, max_value=5, value=1)

    if st.button("Generate"):
        with st.spinner("Generating..."):
            generated_texts = generate_text(model, tokenizer, seed_text, max_length, temperature=1.0, num_return_sequences=2)
            for i, text in enumerate(generated_texts):
                st.write(f"Generated Text {i + 1}:\n{text}\n")

#To create login form:
def login():
    st.subheader(':red[**Login**]')
    with st.form(key='login', clear_on_submit=True):
        username = st.text_input(label='Username', placeholder='Enter Your Username')
        password = st.text_input(label='Password', placeholder='Enter Your Password', type='password')
        if st.form_submit_button('Login'):
            if not username or not password:
                st.error("Please fill out all fields.")
            elif to_verify_user(username, password):
                st.session_state.login_successful = True
                st.session_state.username = username
                st.session_state.current_page = 'home'
                st.rerun()
            else:
                st.error("Incorrect username or password. If you don't have an account, please sign up.")

    #To display signup and reset password button:
    if not st.session_state.login_successful:
        c1, c2 = st.columns(2)
        with c1:
            st.write(":green[New user?]")
            if st.button('Go to Sign Up'):
                st.session_state.current_page = 'sign_up'
                st.rerun()
        with c2:
            st.write(":green[Forgot Password?]")
            if st.button('Reset Password'):
                st.session_state.current_page = 'reset_password'
                st.rerun()

#To create signup form:
def signup():
    st.subheader(':red[**Sign Up**]')
    with st.form(key='signup', clear_on_submit=True):
        email = st.text_input(label='Email', placeholder='Enter Your Email')
        username = st.text_input(label='Username', placeholder='Enter Your Username')
        password = st.text_input(label='Password', placeholder='Enter Your Password', type='password')
        re_password = st.text_input(label='Confirm Password', placeholder='Confirm Your Password', type='password')

        if st.form_submit_button('Sign Up'):
            if not email or not username or not password or not re_password:
                st.error("Please fill out all fields.")
            elif not is_valid_email(email):
                st.error("Please enter a valid email address.")
            elif len(password) <= 3:
                st.error("Password too short")
            elif password != re_password:
                st.error("Passwords do not match. Please re-enter.")
            else:
                result = create_user(username, password, email)
                if result == 'username_data':
                    st.error("Username already registered. Please use a different username.")
                elif result == 'email_data':
                    st.error("Email already registered. Please use a different email.")
                elif result == 'success':
                    st.success(f"Username {username} created successfully! Please login.")
                    st.session_state.sign_up_successful = True
                else:
                    st.error("Failed to create user. Please try again later.")

    if st.session_state.sign_up_successful:
        if st.button('Go to Login'):
            st.session_state.current_page = 'login'
            st.rerun()

#To create reset password page:
def reset_password_page():
    st.subheader(':blue[Reset Password]')
    with st.form(key='reset_password', clear_on_submit=True):
        username = st.text_input(label='Username', value='')
        new_password = st.text_input(label='New Password', type='password')
        re_password = st.text_input(label='Confirm New Password', type='password')

        if st.form_submit_button('Reset Password'):
            if not username:
                st.error("Please enter your username.")
            elif not username_data(username):
                st.error("Username not found. Please enter a valid username.")
            elif not new_password or not re_password:
                st.error("Please fill out all fields.")
            elif len(new_password) <= 3:
                st.error("Password too short")
            elif new_password != re_password:
                st.error("Passwords do not match. Please re-enter.")
            else:
                to_reset_password(username, new_password)
                st.success("Password reset successfully. Please login with your new password.")
                st.session_state.current_page = 'login'

     #button to return to login page:           
    st.write('Return to Login page')
    if st.button('Login'):
        st.session_state.current_page = 'login'
        st.rerun()


# Display appropriate page based on session state
if st.session_state.current_page == 'home':
    home_page()
elif st.session_state.current_page == 'login':
    login()
elif st.session_state.current_page == 'sign_up':
    signup()
elif st.session_state.current_page == 'reset_password':
    reset_password_page()