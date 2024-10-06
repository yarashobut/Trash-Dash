from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4-vision-preview",
  messages=[
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Should I put this in the compost, recycle, or trash? One word answer only."},
        {
          "type": "image_url",
          "image_url": {
            "url": "https://cdn11.bigcommerce.com/s-42uukcbhz8/images/stencil/2560w/products/186/441/cup_clear_pet_16_oz__73148.1631735223.JPG?c=2",
          },
        },
      ],
    }
  ],
  max_tokens=300,
)

print(response.choices[0])
