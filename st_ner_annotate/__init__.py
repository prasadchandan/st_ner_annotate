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
    text = """Manhattan traces its origins to a trading post founded by colonists 
    from the Dutch Republic in 1624 on Lower Manhattan; the post was named New 
    Amsterdam in 1626. Manhattan is historically documented to have been purchased 
    by Dutch colonists from Native Americans in 1626 for 60 guilders, which equals 
    roughly $1059 in current terms. The territory and its surroundings came under 
    English control in 1664 and were renamed New York after King Charles II of 
    England granted the lands to his brother, the Duke of York. New York, based 
    in present-day Manhattan, served as the capital of the United States from 1785 
    until 1790. The Statue of Liberty greeted millions of immigrants as they came 
    to America by ship in the late 19th century and is a world symbol of the United 
    States and its ideals of liberty and peace. Manhattan became a borough during 
    the consolidation of New York City in 1898. 
    """

    nlp = spacy.load("en_core_web_sm")
    entity_labels = nlp.get_pipe('ner').labels

    doc = nlp(text)
    ents = doc.to_json()['ents']

    current_entity_type = st.selectbox("Mark for Entity Type", entity_labels)
    entities = st_ner_annotate(current_entity_type, text, ents, key=42)
    st.json(entities)
