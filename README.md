# Telegu Poetry Generator

This repo hosts code that generates Telegu Poetry with AI and uses Text to Speech to recite the Telegu poetry.This app is hosted [here](https://telegu-poetry.streamlit.app/).

## Getting Started Locally

### Prerequisites

1. Acquire an OpenAI Key by following instructions from here.
2. Acquire an API Key from [Narkeet](https://www.narakeet.com/).
3. Create a Supabase account from [here](https://supabase.com/), create a bucket called "poems" and generate the Supabase Url and Key. Ensure that the policy for the "poem" bucket is set to allow reads, writes, deletes and updates.

### How to Run Locally

1. Ensure you have python 3.8+.
2. Clone the repo: ``git clone https://github.com/MokoSan/TeleguPoetryGenerator``.
3. Install all the prerequistes using ``pip install -r app/requirements.txt`` (preferbly in a virtual environment).
4. Ensure you have streamlit in your path.
5. Copy the .env.example file into a .env file and enter your OpenAI API Key, Narkeet API Key, Supabase Url, Supabase Key.
6. To run: ``streamlit run app/streamlitui.py``.

## Contributions

Contributions are welcomed and encouraged! If you run into any problems, create issues on this repository.

## License

This project is licensed under the [MIT License](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt).