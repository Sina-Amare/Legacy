from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# This import is the key to accessing our environment variables.
from app.core.config import settings

def get_narrative_for_outcome(context: str) -> str:
    """
    Generates a narrative text based on the outcome of a player's decision.

    This function uses LangChain to construct a request to a Large Language Model,
    configured via OpenRouter, to create a rich, story-like text based on the
    provided context of a game event.
    """
    # 1. Initialize the Language Model instance with the corrected parameters.
    # The 'api_key' parameter expects a SecretStr, which we pass directly.
    # The library internally calls .get_secret_value() when making the API request.
    llm = ChatOpenAI(
        model=settings.OPENROUTER_MODEL_NAME,
        api_key=settings.OPENROUTER_API_KEY,
        base_url=settings.OPENROUTER_API_BASE,
        temperature=0.7,
        model_kwargs={
            "max_tokens": 250
        }
    )

    # 2. Define a professional prompt template to guide the AI's response.
    template = """
    شما یک وقایع‌نگار سلطنتی و یک داستان‌سرای ماهر در ایران باستان هستید.
    لحن شما حماسی، ادبی و کمی رسمی است.
    وظیفه شما، روایت کردن وقایع سرنوشت‌ساز پادشاهی در قالب یک پاراگراف است.
    از توصیفات غنی استفاده کنید و به پیامدهای رویداد اشاره کنید.

    رویداد کلیدی: {context}

    روایت شما از این واقعه:
    """
    prompt = PromptTemplate(template=template, input_variables=["context"])
    
    # 3. Create a LangChain chain that combines the prompt and the model.
    narrative_chain = LLMChain(llm=llm, prompt=prompt)
    
    # 4. Invoke the chain and handle potential errors gracefully.
    try:
        response = narrative_chain.invoke({"context": context})
        narrative_text = response.get("text", "روایت این رویداد در غبار تاریخ گم شد...").strip()
        return narrative_text
    except Exception as e:
        print(f"AI narrative generation failed: {e}")
        return "آسمان تاریخ در این لحظه تیره و تار است و وقایع‌نگاران از ثبت آن بازمانده‌اند..."
