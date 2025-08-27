

import streamlit as st
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from string import punctuation
from textblob import TextBlob
import nltk
nltk.download('punkt_tab')
nltk.download('stopwords')
# for summarizing of the text function
def textsummi(text, summary_ratio=0.5):
    sentences = sent_tokenize(text)
    stopwords_lumsum = set(stopwords.words('english') + list(punctuation))
    words = word_tokenize(text.lower())
    words = [w for w in words if w.isalpha() and w not in stopwords_lumsum]

    freq = {}
    for i in words:
        freq[i] = freq.get(i, 0) + 1

    maxfreq = max(freq.values())
    for w in freq:
        freq[w] = freq[w] / maxfreq

    sentences_weights = {}
    for sent in sentences:
        sent_words = word_tokenize(sent.lower())
        score = sum(freq.get(w, 0) for w in sent_words)
        if len(sent_words) > 0:
            sentences_weights[sent] = score / len(sent_words)

    lengthofoutput = max(1, int(len(sentences) * summary_ratio))
    top_sentences = sorted(sentences_weights, key=sentences_weights.get, reverse=True)[:lengthofoutput]
    summary = " ".join([s for s in sentences if s in top_sentences])
    return summary

def sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity
    if polarity > 0:
        label = "Positive 👍😀"
    elif polarity < 0:
        label = "Negative 😒👎"
    else:
        label = "Neutral 😑"
    return polarity, label, subjectivity


st.markdown("<h1 style='text-align: center;'>📖 Text Summarization & Sentiment Analysis</h1>", unsafe_allow_html=True)# title
text = st.text_area("Enter your text here:", height=200)# Input for text
summary_ratio = st.slider("Select summary ratio:", 0.1, 1.0, 0.5)#for selcting thr range of summary ratio

if st.button("Generate Summary & Sentiment"):
    if True:
        summary = textsummi(text, summary_ratio)
        polarity, state ,subjectivity= sentiment(text)
        st.markdown("<h3 style='text-align: center; color: orange;'>Original Text</h3>", unsafe_allow_html=True) # originaltext name heading 
        st.write(text)                  # originaltext

        st.markdown("<h3 style='text-align: center; color: green;'>Summary</h3>", unsafe_allow_html=True)#
        st.markdown(f"<div style='text-align: center;'>{summary}</div>", unsafe_allow_html=True)

        st.markdown("<h3 style='text-align: center; color: orange;'>Polarity & Feedback</h3>", unsafe_allow_html=True)
        # Emoji feedback based on polarity
        if polarity <= -0.6:
            emoji = "😡"
        elif polarity <= -0.2:
            emoji = "😞"
        elif polarity < 0:
            emoji = "😕 "
        elif polarity < 0.2:
            emoji = "😐"
        elif polarity < 0.6:
            emoji = "🙂"
        else:
            emoji = "😄"
        st.markdown(f"<div style='text-align: center;'>{polarity}{emoji}</div>", unsafe_allow_html=True)
        if subjectivity < 0.5:
            gan = "It is Fact 📚"
        elif polarity == 0.5:
            gan = "Half fact 🤷‍♂️half Opinion"
        else:
            gan = "Opinion 🤔"


        st.markdown("<h3 style='text-align: center; color: purple;'>Sentiment State</h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'>{state}</div>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: brown;'>Subjectivity(Fact or Someone's opinion)</h3>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align: center;'>{gan}</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to summarize and analyze.")


