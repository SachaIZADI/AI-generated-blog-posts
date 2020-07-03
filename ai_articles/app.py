import streamlit as st
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import pystache

#  streamlit run app.py


@st.cache(hash_funcs={GPT2Tokenizer: lambda x: 1, GPT2LMHeadModel: lambda x:2})
def load_tokenizer_model():
    tokenizer = GPT2Tokenizer.from_pretrained("output")
    model = GPT2LMHeadModel.from_pretrained("output", pad_token_id=tokenizer.eos_token_id)
    return tokenizer, model


def generate_content(input_str, tokenizer, model):
    input_ids = tokenizer.encode(input_str,return_tensors='pt')

    beam_output = model.generate(
        input_ids,
        max_length=100,
        num_beams=5,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    return tokenizer.decode(beam_output[0], skip_special_tokens=True)

def generate_article(input_str, tokenizer, model):
    content = generate_content(input_str, tokenizer, model)
    with open("medium-copycat/index.html") as f:
        medium_template = f.read()
    return pystache.render(medium_template, {'content': content})


def main():
    tokenizer, model = load_tokenizer_model()

    input_str = st.text_input('Start your article here')
    if not input_str:
        st.text("Write something")
        return

    generated_article = generate_article(input_str, tokenizer, model)
    st.write(generated_article, unsafe_allow_html=True)


main()
