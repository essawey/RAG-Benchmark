import re
import pandas as pd
from datasets import load_dataset

narrativeqa = load_dataset("deepmind/narrativeqa")

rows = []
document_obj = narrativeqa['train']['document']
answer_objs = narrativeqa['train']['answers']
question_obj = narrativeqa['train']['question']

from bs4 import BeautifulSoup
from tqdm import tqdm

for i in tqdm(range(len(document_obj)-1)):

    question = question_obj[i]
    answer = answer_objs[i][0] # Taking the fisrt answer
    document = document_obj[i]

    question = question['text'].lower()
    answer = answer['text'].lower()
    document = document['text'].lower()
    document = re.sub(r'\n+', ' ', document)

    question = re.sub(r'\s+', ' ', question)
    answer = re.sub(r'\s+', ' ', answer)
    document = re.sub(r'\s+', ' ', document)

    if '<html>' in document:
      document_soup = BeautifulSoup(document, "html.parser")
      document = document_soup.get_text()

    rows.append([
        question,
        answer,
        document,
    ])

df = pd.DataFrame(rows, columns=['question', 'answer', 'document'])

df = df[df.apply(lambda row: len(row['answer'].strip().split()) > 2, axis=1)]
df = df[df.apply(lambda row: row['document'].count(row['answer'].strip()) == 1, axis=1)]

df = df.reset_index(drop=True)
df = df.drop_duplicates()

def get_rag_context(row, window_size=1):
    answer = row['answer'].strip()
    document = row['document']

    # Split the document into sentences
    sentences = re.split(r'(?<=[.!?])', document)

    # Search for the sentence that contains the answer
    for idx, sentence in enumerate(sentences):
        if answer in sentence:
            start = max(0, idx - window_size)
            end = min(len(sentences), idx + window_size + 1)
            context = ''.join(sentences[start:end])
            return context


df['rag_context'] = df.apply(get_rag_context, axis=1)

df = (
    df.assign(answer_word_count=df['answer'].apply(lambda x: len(str(x).split())))
      .sort_values(by='answer_word_count', ascending=False)
      .drop(columns=['answer_word_count'])
      .reset_index(drop=True)
)

df.to_excel('RAG Benchmark.xlsx')
