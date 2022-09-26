import os
import json
import spacy
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

_RELEASE = False
st.session_state.update(st.session_state)
if 'page_number' not in st.session_state:
    st.session_state.page_number = 0
with open('../data/test.food.cml.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

if not _RELEASE:
    _component_func = components.declare_component(
        "st_ner_annotate", url="http://localhost:5000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/public")
    _component_func = components.declare_component(
        "st_ner_annotate", path=build_dir)


def st_ner_annotate(label, text, ents, key=None):
    """st_edit_named_entities.

    Parameters
    ----------
    text: str
        Text to render
    ents: object
        Entities found in text
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    object
        Entities that have been selected
    """
    component_value = _component_func(
        label=label, text=text, ents=ents, key=key, default=ents)

    return component_value


def get_label_entities(doc, wordlist, label):
    result = []
    for word in wordlist:
        if 'wizard' in word.lower() or 'apprentice' in word.lower():
            continue
        result.append({'start': doc.find(word), 'end': doc.find(word) + len(word), 'label': label, 'word': word})
    return result


# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    st.markdown("# Demonstrating use of Next button with Session State")

    # A variable to keep track of which product we are currently displaying
    # session_state = st.session_state.get(page_number=0)

    last_page = len(data)

    # Add a next button and a previous button
    # data_id = st.text_input('Data ID', 0)
    # data_id = int(data_id)

    prev, _, next = st.columns([1, 10, 1])
    # if data_id > last_page:
    #     st.session_state.page_number = 0
    # else:
    #     st.session_state.page_number = data_id
    if next.button("Next"):
        if st.session_state["page_number"] + 1 > last_page:
            st.session_state.page_number = 0
        else:
            st.session_state.page_number += 1

    if prev.button("Previous"):

        if st.session_state["page_number"] - 1 < 0:
            st.session_state.page_number = last_page
        else:
            st.session_state.page_number -= 1

    # Get start and end indices of the next page of the dataframe
    data_id = st.session_state["page_number"]

    # Index into the sub dataframe
    # sub_df = data[data_id]

    # data_id = st.text_input('Data ID', 0)
    # st.write('Document ID is', data_id)
    # data_id = int(data_id)
    st.title("CML tagging demo")
    text = data[data_id]['dialog']
    # PP_ents = [{} for word in data[data_id]['sent_index']]
    WP_ents = get_label_entities(text, data[data_id]['keywords']['positive'], 'WP')
    print(text)
    entity_labels = ['WP', 'PP']
    ents = WP_ents if len(WP_ents) <= 10 else WP_ents[:10]
    current_entity_type = st.selectbox("Mark for Entity Type", entity_labels)
    entities = st_ner_annotate(current_entity_type, text, ents)
    # st.json(entities)
