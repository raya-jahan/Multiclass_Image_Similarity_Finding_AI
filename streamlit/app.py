# from qdrant_client import QdrantClient

# from io import BytesIO
# import streamlit as st
# import base64
# from qdrant_client.models import Filter, FieldCondition, MatchValue

# import qdrant_client 



# collection_name ="animal_images"
# st.title("Multiclass Image Similarity Search")
# selected_type = st.selectbox("Choose image category", ["cat", "dog", "wild"])
# st.subheader(f"Showing {selected_type.upper()} images")



# if 'selected_record' not in st.session_state:
#     st.session_state.selected_record = None
    

# def set_selected_record(new_record):
#     st.session_state.selected_record = new_record


# @st.cache_resource
# def get_client():
#     return QdrantClient(
        
#         url=st.secrets.get("qdrant_db_url"),
#         api_key=st.secrets.get("qdrant_api_key"),
    
# )

        
    


# # def get_initial_records(type_filter):

# #     client = get_client()
# #     records, _ = client.scroll(
# #         collection_name=collection_name,
# #         with_vectors=False,
# #         limit=12,
# #         filter=Filter(
# #             must=[
# #                 FieldCondition(
# #                     key="type",
# #                     match=MatchValue(value=type_filter)
# #                 )
# #             ]
# #         )
# #     )
    
    
    
# #     return records


# def get_initial_records(type_filter):
#     client = get_client()
    
#     all_records, _ = client.scroll(
#         collection_name=collection_name,
#         with_vectors=False,
#         limit=1000  # pull more so we can filter in Python
#     )

    
#     filtered = [r for r in all_records if r.payload.get("type") == type_filter]
#     return filtered[:12]  # just return first 12 after filter



# def get_similar_records(type_filter):
#     client = get_client()
    
#     if st.session_state.selected_record is not None:
#         similar = client.recommend(
#             collection_name=collection_name,
#             positive=[st.session_state.selected_record.id],
#             limit=50  # get more to filter from
#         )
#         # filter manually based on class
#         return [r for r in similar if r.payload.get("type") == type_filter]
#     return []



# def get_bytes_from_base64(base64_string):
#     return BytesIO(base64.b64decode(base64_string))


# records = get_similar_records(type_filter=selected_type) if st.session_state.selected_record is not None else get_initial_records(type_filter=selected_type)


# if not records:
#     st.warning(f"No {selected_type} images found.")


# if st.session_state.selected_record:
#     image_bytes = get_bytes_from_base64(
#         st.session_state.selected_record.payload["base64"])
#     st.header("Images similar to:")
#     st.image(
#         image=image_bytes
#     )
#     st.divider()
    

# columns = st.columns(3)
# # for idx, record in enumerate(records):
# #     col_idx = idx % 3
# #     image_bytes = get_bytes_from_base64(record.payload["base64"])
# #     with column[col_idx]:
# #         st.image(image=image_bytes)
# #         st.button(
# #             label="Find similar images",
# #             key=record.id,
# #             on_click=set_selected_record,
# #             args=[record]
# #         )

# for idx, record in enumerate(records):
#     st.write(record.payload)
#     if "base64" not in record.payload:
#         continue  # skip if image is broken or missing
    
#     col = columns[idx % 3]
#     with col:
#         image_bytes = get_bytes_from_base64(record.payload["base64"])
#         st.image(image_bytes)
#         st.button(
#             label="Find similar images",
#             key=record.id,
#             on_click=set_selected_record,
#             args=[record]
#         )



from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue

import streamlit as st
from io import BytesIO
import base64

collection_name = "animal_images"

st.set_page_config(page_title="Multiclass Image Similarity AI", layout="wide")
st.title("Multiclass Image Similarity Search")
selected_type = st.selectbox("Choose image category", ["cat", "dog", "wild"])
st.subheader(f"Showing {selected_type.upper()} images")

if 'selected_record' not in st.session_state:
    st.session_state.selected_record = None

def set_selected_record(new_record):
    st.session_state.selected_record = new_record

@st.cache_resource
def get_client():
    return QdrantClient(
        url=st.secrets.get("qdrant_db_url"),
        api_key=st.secrets.get("qdrant_api_key")
    )

def get_initial_records(type_filter):
    client = get_client()
    all_records, _ = client.scroll(
        collection_name=collection_name,
        with_vectors=False,
        limit=1000
    )
    filtered = [r for r in all_records if r.payload.get("type") == type_filter]
    return filtered[:12]

def get_similar_records(type_filter):
    client = get_client()
    if st.session_state.selected_record:
        similar = client.recommend(
            collection_name=collection_name,
            positive=[st.session_state.selected_record.id],
            limit=50
        )
        return [r for r in similar if r.payload.get("type") == type_filter]
    return []

def get_bytes_from_base64(base64_string):
    return BytesIO(base64.b64decode(base64_string))

records = get_similar_records(type_filter=selected_type) if st.session_state.selected_record else get_initial_records(type_filter=selected_type)

if not records:
    st.warning(f"No {selected_type} images found.")

if st.session_state.selected_record:
    image_bytes = get_bytes_from_base64(st.session_state.selected_record.payload["base64"])
    st.header("Images similar to:")
    st.image(image=image_bytes)
    st.divider()

columns = st.columns(3)

for idx, record in enumerate(records):
    if "base64" not in record.payload:
        continue
    col = columns[idx % 3]
    with col:
        image_bytes = get_bytes_from_base64(record.payload["base64"])
        st.image(image_bytes)
        st.button(
            label="Find similar images",
            key=record.id,
            on_click=set_selected_record,
            args=[record]
        )
