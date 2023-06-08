import os
import openai
import gradio as gr

# openai and gradio two libraries we require to run this application

# API key generated on website https://platform.openai.com/account/api-keys
openai.api_key = "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"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: "


def openai_create(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=4000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    return response.choices[0].text

# function define
# input for gradio
# for gradio application to work anything that has to be wrapped inside the function and
# that function should have an input that function should have an output
# one or more inputs..in this here input is a text

# history stores the state of the current gradio application
def chatgpt_clone(input, history):
    # if history doesn't exist then it will be empty []
    history = history or []

    # take history convert to list
    s = list(sum(history, ()))

    # append the current input to history
    s.append(input)

    # store in inp
    inp = ' '.join(s)

    # generate response by openai_create function and response get store in output
    output = openai_create(inp)

    # history append one input and output
    history.append((input, output))

    # store as history, history then get displayed
    return history, history

# to display as msg box we are using blocks which is advanced method to create gradio application
# block bcoz it gives the chatGPT style interface like from top to bottom
block = gr.Blocks()

# in block
with block:

    # Title of block
    gr.Markdown("""<h1><center> Alisha Chatbot </center></h1>
    """)
    # we need chatbot
    chatbot = gr.Chatbot()

    # we need input textbox
    # prompt for msg to keep in start
    message = gr.Textbox(placeholder=prompt)

    # to store the state
    state = gr.State()

    # button to click send
    submit = gr.Button("SEND")

    # take input
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])

# this will launch our application
block.launch(debug=True)
