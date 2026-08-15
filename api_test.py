from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-5-mini",
    input="Say hello to Nova in one short sentence."
)

print(response.output_text)