import openai
import streamlit as st
import json
from datetime import datetime
import config
import logging
from streamlit.runtime.scriptrunner import get_script_run_ctx
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

st.title("BIGDaTA_Lab Chatbot")
openai.api_key = "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"
logging.basicConfig(filename='C:\\Users\\Ali Onur\\Desktop\\finbot\\logs\\stockGPT.logstockGPT.log',
                    level=logging.INFO, format='%(asctime)s - %(message)s', encoding='utf-8')  # encoding ekleyin

CPI_Data_Address = "C:\\Users\\Ali Onur\\Desktop\\finbot\\finance-cbot\\CPI_DATA.xls"

# Veriyi yükle
with open('C:\\Users\\Ali Onur\\Desktop\\finbot\\finance-cbot\\training_data.json', 'r', encoding='utf-8') as f:
    veri = json.load(f)
with open('C:\\Users\\Ali Onur\\Desktop\\finbot\\finance-cbot\\hesap_botu.json', 'r', encoding='utf-8') as f:
    veri2 = json.load(f)


def get_stock_price(ticker):
    try:
        return str(yf.Ticker(ticker).history(period="1m").iloc[-1].Close)
    except Exception as e:
        return f"Veri alınırken bir hata oluştu: {e}"


def get_CPI(country_code, year, month):
    # Get Consumer Price Index
    data_file = pd.read_excel(CPI_Data_Address, sheet_name=country_code, header=None)
    cell_value = data_file.iloc[int(year) - 1999, int(month)]
    return str(cell_value)


def plot_CPI(country_code, start_year, start_year_month, end_year, end_year_month):
    # TODO
    # data = yf.Ticker(ticker).history(period="1y")
    # plt.figure(figsize=(10, 5))
    # plt.plot(data.index, data.Close)
    # plt.title(f'{ticker} Geçen Yıla Göre Hisse Fiyatı')
    # plt.xlabel('Tarih')
    # plt.ylabel('Hisse Fiyatı ')
    # plt.grid(True)
    # plt.savefig('stock.png')
    # plt.close()
    return 0


def calculate_SMA(ticker, window):
    data = yf.Ticker(ticker).history(period="1y").Close
    if len(data) < window:
        return f"Hata: '{ticker}' için yeterli veri yok. En az {window} veri gerekiyor."
    return str(data.rolling(window=window).mean().iloc[-1])


def calculate_EMA(ticker, window):
    data = yf.Ticker(ticker).history(period="1y").Close
    return str(data.ewm(span=window, adjust=False).mean().iloc[-1])


def calculate_RSI(ticker):
    data = yf.Ticker(ticker).history(period="1m").Close
    delta = data.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ema_up = up.ewm(com=14 - 1, adjust=False).mean()
    ema_down = down.ewm(com=14 - 1, adjust=False).mean()
    rs = ema_up / ema_down
    return str(100 - (100 / (1 + rs)).iloc[-1])


def calculate_MACD(ticker):
    data = yf.Ticker(ticker).history(period="1y").Close
    short_EMA = data.ewm(span=12, adjust=False).mean()
    long_EMA = data.ewm(span=26, adjust=False).mean()

    MACD = short_EMA - long_EMA
    signal = MACD.ewm(span=9, adjust=False).mean()
    MACD_histogram = MACD - signal

    return f'{MACD[-1]},{signal[-1]},{MACD_histogram[-1]}'


def plot_stock_price(ticker):
    data = yf.Ticker(ticker).history(period="1y")
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data.Close)
    plt.title(f'{ticker} Geçen Yıla Göre Hisse Fiyatı')
    plt.xlabel('Tarih')
    plt.ylabel('Hisse Fiyatı ')
    plt.grid(True)
    plt.savefig('stock.png')
    plt.close()


def report():
    return ("Enes Uzun & Ali Onur Aslan tarafından raporlanmıştır.")


available_fuctions = {
    'get_stock_price': get_stock_price,
    'calculate_SMA': calculate_SMA,
    'calculate_EMA': calculate_EMA,
    'calculate_RSI': calculate_RSI,
    'calculate_MACD': calculate_MACD,
    'plot_stock_price': plot_stock_price,
    'get_CPI': get_CPI,
    'report': report
}

functions = [
    {
        'name': 'get_CPI',
        'description': 'Gets the consumer price index of country in the given time',
        'parameters': {
            'type': 'object',
            'properties': {
                'country_code': {
                    'type': 'string',
                    'description': 'Country code of the country, (for exmple TR for Turkey, and NL for the Netherlands)'

                },
                'year': {
                    'type': 'string',
                    'description': "This value represents the desired year of the CPI value for the desired country"

                },
                'month': {
                    'type': 'string',
                    'description': "This value represents the numerical value of desired month of the CPI value for the desired country. (Ex. 7 for july)"

                },
            },
            'required': ['country_code']

        }
    },
    {
        'name': 'get_stock_price',
        'description': 'Gets the latest stock price given the ticker symbol of a company.',
        'parameters': {
            'type': 'object',
            'properties': {
                'ticker': {
                    'type': 'string',
                    'description': 'The stock ticker symbol for a company (for example AAPL for Apple).'

                },
            },
            'required': ['ticker']

        }
    },
    {
        "name": "calculate_SMA",
        "description": "Calculate the simple moving average for a given stock ticker and a window.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company (e.g., AAPL for Apple)",
                },
                "window": {
                    "type": "integer",
                    "description": "The timeframe to consider when calculating the SMA"
                },
            },
            "required": ["ticker", "window"],
        },
    },
    {
        "name": "calculate_EMA",
        "description": "Calculate the exponential moving average for a given stock ticker and a window",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company(e.g., APPL for Apple)",
                },
                "window": {
                    "type": "integer",
                    "description": "The timeframe to consider when calculating EMA"
                }
            },
            "required": ["ticker", "window"],
        },

    },
    {
        "name": "calculate_RSI",
        "description": "Calculate the RSI for a given stock ticker",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company(e.g., APPL for Apple)",
                },
            },
            "required": ["ticker"],
        },

    },
    {
        "name": "calculate_MACD",
        "description": "Calculate the MACD for a given stock ticker.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company(e.g., APPL for Apple)",
                },
            },
            "required": ["ticker"],
        },

    },
    {
        "name": "plot_stock_price",
        "description": "Plot the stock price for the last year given the ticker symbol of a company.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "The stock ticker symbol for a company(e.g., APPL for Apple)",
                },
            },
            "required": ["ticker"],
        },
    },
    {
        "name": "report",
        "description": "Print the report about football",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Print report about football",
                },
            },
            "required": [],
        },
    },
]


def chat_with_gpt3(message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        # ft:gpt-3.5-turbo-1106:yat-r-m-finansman::8a5s7YU0
        # gpt-4-1106-preview
        messages=[
            {"role": "system", "content": veri},
            {"role": "system",
             "content": "Sen bir BigDataLab Finans Chat botusun. Tüm cevapları ona göre vermelisin."},
            {"role": "system", "content": veri2},
            {"role": "user", "content": message}
        ],
        temperature=0.4,
        max_tokens=1000,
        functions=functions,
        function_call='auto'
    )
    if "rapor" in message:
        print("enesenes")

    user_message = message

    logging.info(f"Kullanıcı: {user_message}")

    assistant_response = response.choices[0].message['content']
    logging.info(f"Asistan: {assistant_response}")

    return response.choices[0].message['content']


if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Selam! Nasıl yardımcı olabilirim?"):
    start_time = datetime.now()

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        response = openai.ChatCompletion.create(
            model="gpt-4-1106-preview",
            # ft:gpt-3.5-turbo-1106:yat-r-m-finansman::8a5s7YU0
            messages=[
                {"role": "system", "content": veri},
                {"role": "system", "content": veri2},
                {"role": "system",
                 "content": "Sen bir BIGDaTA_Lab Finans Chat botusun. Sen Ekonomi ve Finans alanında uzmansın.Kısa "
                            "cevap ver.Tüm "
                            "cevapları "
                            "ona "
                            "göre vermelisin."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=1000,
            functions=functions,
            function_call='auto'
        )

        user_message = prompt
        logging.info(f"Kullanıcı: {user_message}")

        assistant_response = response.choices[0].message['content']
        logging.info(f"Asistan: {assistant_response}")

        response_message = response['choices'][0]['message']

        if response_message.get('function_call'):
            function_name = response_message['function_call']['name']
            function_args = json.loads(response_message['function_call']['arguments'])
            if function_name in ['get_stock_price', 'calculate_RSI', 'calculate_MACD', 'plot_stock_price', ]:
                args_dict = {'ticker': function_args.get('ticker')}
            elif function_name in ['calculate_SMA', 'calculate_EMA']:
                args_dict = {'ticker': function_args.get('ticker'), 'window': function_args.get('window')}
            elif function_name in ['get_CPI']:

                year_value = function_args.get('year')
                if year_value is None:
                    year_value = 2024
                month_value = function_args.get('month')
                if month_value is None:
                    month_value = 1

                args_dict = {'country_code': function_args.get('country_code'), 'year': year_value,
                             'month': month_value}
            elif function_name in ['report']:
                args_dict = {}

            function_to_call = available_fuctions[function_name]
            function_response = function_to_call(**args_dict)

            if function_name == 'plot_stock_price':
                st.image('stock.png')
            else:
                st.session_state['messages'].append(response_message)
                st.session_state['messages'].append(
                    {
                        'role': 'function',
                        'name': function_name,
                        'content': function_response
                    }
                )  # ft:gpt-3.5-turbo-1106:yat-r-m-finansman::8a5s7YU0
                second_response = openai.ChatCompletion.create(
                    model='gpt-4-1106-preview',
                    messages=st.session_state['messages']
                )
                st.text(second_response['choices'][0]['message']['content'])
                st.session_state['messages'].append(
                    {'role': 'assistant', 'content': second_response['choices'][0]['message']['content']})
        else:
            response_content = response.choices[0].message['content']

            elapsed_time = datetime.now() - start_time
            response_seconds = elapsed_time.total_seconds()

            apology_message = "Biraz uzun sürdüğü için kusura bakmayın.<br>" if response_seconds > 900 else ""

            response_for_display = f"{response_content}<br><div style='text-align:right; font-size:0.8em;'>{apology_message} {response_seconds:.2f} saniye</div>"
            st.markdown(response_for_display, unsafe_allow_html=True)

            response_for_state = f"{response_content} {apology_message} {response_seconds:.2f} saniye"
            st.session_state.messages.append({"role": "assistant", "content": response_for_state})
