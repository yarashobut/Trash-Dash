import gradio as gr
from openai import OpenAI
import base64
client = OpenAI()
rules = """Should I recycle,compost, or trash the elements in the pictures? Give a sentence answer saying what to do with each element, then give a short explanation of your answers. These are the rules that should guide in making your decision.I will provide you with information including the item that might be in the picture and information about it. 
Aluminum foil is Recycled. Rinse or wipe off food and liquid first.
Baked goods are Compostable. All food scraps (including meat and dairy) are compostable.
Aluminum Cans are Recycled. The can must be Empty and clean of food and beverage before recycling.
Cardboard is recyclable. It must be broken down with the tape removed before discarding.
Cartons are recyclable
Chopsticks are compostable if the item is wood or was provided by the College.
Coffee filters are compostable
Coffee sleeves are compostable if provided by the college
Coffee stirrers are compostable if they are wood or provided by the college
Cold Drink Cups are Compostable if they were provided by the College and have a GREENWARE label.
Cold Drink Cup Lid are Compostable if the item was provided by the College and has a GREENWARE label.
Compostable Utensils are Compostable  
paper-based bags  are compostable. 
Paper-based napkins are compostable.
Envelopes are recyclable, even with plastic windows
Fruits and vegetables are compostable 
Glass, Bottles and Jars are Recyclable if they are unbroken, clean, and empty. 
Broken glass is trash
Hot Drink Cups are Compostable if the item was provided by the College and has ECOCONTAINER label
Hot Drink Cup Lids are Compostable if item was provided by the College
Magazines are recycled if they are made of glossy material and Compostable if they are made of non-glossy paper.
Paper napkins used with chemicals or cleaners are Trash only
Newspapers are recyclable 
Notebooks are recycled
Padded Envelope are trash
Paper bags are recycled
Paper clips are recycled
Paper Plates and Bowls are Composted if they were provided by the College, Recycled if not College-provided but made of paper. And Trash  if not College-provided and has waxy finish. 
Paper Towels are Compost. However, if used for chemicals or cleaners, they are trash
Pills or medicine are trash
Pizza is Composted. Cheese and meat toppings are compostable.
Pizza boxes are Compost, but remove wax lining in box
Plastic Bag, Film, or Saran Wrap are trash unless the  grocery store recycles plastic bags, and many do!
Plastic Bottle or Jugs are Recycled if item is made of plastic #1, #2, or #5. Make sure it is empty and clean. The item is trashed if made of plastic #3, #4, or #6.
Plastic Salad Containers are Recycled if the item is made of plastic #1, #2, or #5. Make sure it's empty and clean. They are Composted if item is #7 or PLA plastic. they are Trash if the item is #3, #4, or #6
Plastic Takeout Containers are Recycled if item is made of plastic #1, #2, #5. They are Trash if made of black plastic.
Plastic Containers and/or Lids are Recycled if item is made of plastic #1, #2, #5.  Make sure it is empty and clean. They are Trash if item is unlabeled or  #3, #4,or #6.
Plastic Utensils are Trash if item is plastic and unlabeled or #3, #4 or #6. 
Sandwiches are Composted. Meat and cheese and spread fillings are okay.
Scrap paper is recycled 
Shredded paper is composted
Snack Bar Wrapper is trash
Solo cups are trash
Staples are trash
Paper straws are Compostable if provided by the College.
Styrofoam is trash
Sugar, Salt, or Sweetener Packets are compostable if the packet is paper
Takeout Containers are Composted if they are provided by the College. Recycled if made of paper. And Trashed if they are Styrofoam.
Takeout Lunch Boxes are Recycled if provided by the College. 
Tea bags are composted if you remove the staple on them 
Tea bag wrappers are Recycled if made of glossy material and Composted if made of paper.
These are places on campus where you should put corresponding elements:
ELECTRONICS can be donated to the Worthmore free store year-round.

"""
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
  
def checkQuestion(image):
    base64_image = encode_image(image)
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": rules},
            {
            "type": "image_url",
            "image_url": {
                 "url": f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )

    return response.choices[0].message.content
def generalQuestion(image,question):
    base64_image = encode_image(image)
    response = client.chat.completions.create(
    model="gpt-4-vision-preview",
    messages=[
        {
        "role": "user",
        "content": [
            {"type": "text", "text": question},
            {
            "type": "image_url",
            "image_url": {
                 "url": f"data:image/jpeg;base64,{base64_image}"
            },
            },
        ],
        }
    ],
    max_tokens=300,
    )

    return response.choices[0].message.content

with gr.Blocks() as demo:
    image_input=gr.Image(type="filepath", height=700, container="true")
    user_input=gr.Textbox(label="question")
    output = gr.Textbox(label="Output Box")
    submit_btn = gr.Button("Ask The Question")
    submit_btn.click(fn=generalQuestion, inputs=[image_input, user_input], outputs=output, api_name="greet")

if __name__ == "__main__":
    demo.launch()