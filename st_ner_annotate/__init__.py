import os
import spacy
import streamlit.components.v1 as components

_RELEASE = True

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

# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    st.title("Named entity recognition demo")
    text = "Google was founded in September 1998 by Larry Page and Sergey Brin while they were Ph.D. students at Stanford University in California. Together they own about 14 percent of its shares and control 56 percent of the stockholder voting power through supervoting stock. They incorporated Google as a California privately held company on September 4, 1998, in California. Google was then reincorporated in Delaware on October 22, 2002 by Me."
    nlp = spacy.load("en_core_web_sm")
    entity_labels = nlp.get_pipe('ner').labels

    doc = nlp(text)
    ents = doc.to_json()['ents']

    current_entity_type = st.selectbox("Mark for Entity Type", entity_labels)
    entities = st_ner_annotate(current_entity_type, text, ents, key=42)
    st.json(entities)
