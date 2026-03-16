#state_tool.py

def get_top_states(data: dict, top_n=5):
    states_df = data["states"]
    return states_df.head(top_n).to_dict()