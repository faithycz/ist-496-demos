from common.utils import setup, prompt_llm

def main():
    parameters = {
        "api_key": "GEMINI_API_KEY",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/"
    }

    setup(parameters["api_key"])

    model_list = ["models/gemini-3.1-flash-lite"]
    question_list = [
        "What is 1 + 1?",
        "What is the value of pi?"
    ]

    for model in model_list:
        for question in question_list:
            resp = prompt_llm(model, question, **parameters)
            print("=================================")
            print(model)
            print(question)
            print(resp)

if __name__ == "__main__":
    main()