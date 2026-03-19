import ollama

def generate_answer(context, query):

    try:
        response = ollama.chat(
            model="phi3:mini",
            messages=[
                {
                    "role": "user",
                    "content": f"{query}\n\nContext:\n{context}"
                }
            ],
            options={
                "temperature": 0.3
            }
        )

        return response.get("message", {}).get("content", None)

    except Exception as e:
        print("❌ OLLAMA ERROR:", str(e))
        return None