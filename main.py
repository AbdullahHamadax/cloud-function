from openai import OpenAI
import base64
import json
import os


def main(context):

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

    if not context.req.body:
        return context.res.json({"error": "No image provided"}, status_code=400)

    try:
        image_data = context.req.body

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze this image and get recipes based on it",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_data,
                                "detail": "low",
                            },
                        }
                    ],
                },
            ],
        )

        suggestions = response.choices[0]
        context.log(suggestions)
        
        return context.res.json({"recipes": suggestions.content})
    except Exception as e:
        context.log(e)
        return context.res.json({"error": str(e)})