from dotenv import load_dotenv
from langchain.messages import HumanMessage
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver

MODEL="gpt-5-mini"

class State(TypedDict):
    messages: Annotated[list,add_messages]

llm=ChatOpenAI(model=MODEL)

def pick_a_topic(state: State)->dict:
    state["messages"].append({"role":"user","content": "choose a random topic. Reply in one word. Use the last one if one was chosen before"})
    response=llm.invoke(state["messages"])
    print(f"Topic chosen: {response.content}")
    return {"messages":[response]} 

def make_a_positive_argument(state: State)->dict:
    state["messages"].append(HumanMessage("make a positive argument on the topic"))
    response=llm.invoke(state["messages"])
    print(f"Argument: {response.content}")
    return {"messages":[response]} 

def counter_the_argument(state: State)->dict:
    state["messages"].append(HumanMessage("counter the argument"))
    response=llm.invoke(state["messages"])
    print(f"Counter: {response.content}")
    return {"messages":[response]} 

def counter_the_counter(state: State)->dict:
    state["messages"].append(HumanMessage("counter the counter"))
    response=llm.invoke(state["messages"])
    print(f"Argument : {response.content}")
    return {"messages":[response]} 

def reach_on_a_settlement(state: State)->dict:
    state["messages"].append(HumanMessage("reach on a settlement"))
    response=llm.invoke(state["messages"])
    print(f"Agreement: {response.content}")
    return {"messages":[response]} 


memory = MemorySaver()

builder=StateGraph(State)
builder.add_node("pick_a_topic",pick_a_topic)
builder.add_node("make_a_positive_argument",make_a_positive_argument)
builder.add_node("counter_the_argument",counter_the_argument)
builder.add_node("counter_the_counter",counter_the_counter)
builder.add_node("reach_on_a_settlement",reach_on_a_settlement)

builder.add_edge(START,"pick_a_topic")
builder.add_edge("pick_a_topic","make_a_positive_argument")
builder.add_edge("make_a_positive_argument","counter_the_argument")
builder.add_edge("counter_the_argument","counter_the_counter")
builder.add_edge("counter_the_counter","reach_on_a_settlement")
builder.add_edge("reach_on_a_settlement",END)

graph = builder.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "conversation-1"}}

graph.invoke({"messages":[{"role":"system","content":"You are a wise person. You will respond with just a one-liner always"}]},config)

print("\nsnapshot of the current is shown below")
print("="*30)
snapshot=graph.get_state(config)
messages=snapshot.values["messages"]
for message in messages:
    print(message.content)


print("\ncheckpoints are as below")
print("="*30)

checkpoints=list(graph.get_state_history(config))
print(f"Mumber of checkpoints:{len(checkpoints)}")

ctr=0
agreement_checkpoint={}
for checkpoint in reversed(checkpoints):
    ctr+=1
    print(f"checkpoint {ctr}")
    print("-"*30)
    metadata=checkpoint.metadata
    if(len(checkpoint.tasks)>0 and checkpoint.tasks[-1].name=="reach_on_a_settlement"):
        agreement_checkpoint=checkpoint
    queued=",".join(t.name for t in checkpoint.tasks) or "(run complete)"
    print(f"step {metadata["step"]:>2} {metadata["source"]:<5} messages={len(checkpoint.values.get('messages',[]))} about to run {queued}")

replay_config={"configurable": {"thread_id": "conversation-1","checkpoint_id":agreement_checkpoint.config["configurable"]["checkpoint_id"]}}
#graph.invoke({"messages":[{"role":"user","content":"Lets continue on the last topic, don't choose new one"}]},config)
graph.invoke(None,replay_config)
