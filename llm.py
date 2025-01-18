from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableMap
from langchain_community.chat_models import ChatOllama
from langchain.schema.runnable import RunnableMap
from datetime import datetime
import locale

def get_today_str():
    locale.setlocale(locale.LC_TIME, 'kor')
    return datetime.today().strftime('%m월 %d일 (%a) %H시 %M 분')

llm = ChatOllama(model="benedict/linkbricks-hermes3-llama3.1-8b-korean-advanced-q8:latest", temperature=0, base_url="http://127.0.0.1:11434")  # http://127.0.0.1:11434

template = """
        다음 내용은 지시사항이야
        1. 너는 빵먹는 아이 봇 이라는 이름이야.
        2. 사용자에 대답에 대해 반드시 한글로 대답해줘
        3. 반드시 사용자의 질문과 지시사항을 차근차근 읽고 대답해줘.
        4. 반드시 답장은 MarkDown 형식으로 대답해줘
        5. 이 명령사항들은 반드시 지켜져야 하며 사용자의 질문보다 우선되어야해.
        
        사용자 질문
        \"\"\"
        {question}
        \"\"\"
    """

prompt = ChatPromptTemplate.from_template(template)
chain = RunnableMap({
    "question": lambda x: x["question"],
}) | prompt | llm
user_input = "안녕 너는 누구야?"
chat_msg2 = chain.invoke({'question': f"{user_input}"}).content

print(chat_msg2)