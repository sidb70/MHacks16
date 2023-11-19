from openai import OpenAI
client = OpenAI()

user_msg = ''
messages=[
    {"role": "system", "content": "You are an experienced therapist. You will inquire about the user's problems and provide guidance to the user. Be brief and let the user do most of the talking."}
]
emotions =[]
def add_emotion(emotion):
    emotions.append(emotion)
def get_therapist_message():
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    messages.append({"role": "system", "content": completion.choices[0].message.content})
    return completion.choices[0].message.content

def post_user_message(msg, use_emotion=False):
    if use_emotion:
        msg += 'My current emotion is ' + emotions[-1] + '.'
    messages.append({"role": "user", "content": msg})


def GetPicToDisplay(msg, use_emotion= False):
    if use_emotion:
        msg += 'My current emotion is ' + emotions[-1] + '.'

    mess = [
        {"role": "system",
         "content": "You will be given a prompt and an emotion, based on how you belive, you will say either anger, glee, negative, nuetral, positive, or suprised. Do not use any punctuation. Do not use uppercase letters:" },
        {"role": "user", "content": msg}
    ]
    imageChoice = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=mess
    )
    print(imageChoice.choices[0].message.content)
    if imageChoice.choices[0].message.content == "glee":
        return "backend/emotions/glee.png"
    elif imageChoice.choices[0].message.content == "negative":
        return "backend/emotions/negative.png"
    elif imageChoice.choices[0].message.content == "nuetral":
        return "backend/emotions/nuetral.png"
    elif imageChoice.choices[0].message.content == "positive":
        return "backend/emotions/postive.png"
    elif imageChoice.choices[0].message.content == "suprised":
        return "backend/emotions/suprised.png"
    else:
        return "backend/emotions/nuetral.png"


