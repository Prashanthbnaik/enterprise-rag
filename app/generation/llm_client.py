from groq import Groq
import time
import traceback


class GroqLLMClient:

    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.3-70b-versatile",
        max_retries: int = 3
    ):

        if not api_key:
            raise ValueError("GROQ_API_KEY missing")

        self.client = Groq(api_key=api_key)

        self.model = model

        self.max_retries = max_retries


    def generate(

        self,
        prompt: str,
        temperature: float = 0,
        max_tokens: int = 400

    ):

        start_time = time.time()

        last_error = None


        for attempt in range(self.max_retries):

            try:

                response = self.client.chat.completions.create(

                    model=self.model,

                    messages=[

                        {
                            "role": "system",
                            "content":
                            (
                                "You are an enterprise retrieval-augmented "
                                "assistant. Answer ONLY using provided context."
                            )
                        },

                        {
                            "role": "user",
                            "content": prompt
                        }

                    ],

                    temperature=temperature,

                    max_tokens=max_tokens

                )


                latency = round(
                    time.time() - start_time,
                    3
                )


                return {

                    "text":
                        response.choices[0]
                        .message
                        .content
                        .strip(),

                    "latency": latency

                }


            except Exception as e:

                last_error = e

                time.sleep(1)


        print("LLM ERROR:", traceback.format_exc())


        return {

            "text":
                "Model unavailable. Please try again.",

            "latency":
                round(time.time() - start_time, 3)

        }