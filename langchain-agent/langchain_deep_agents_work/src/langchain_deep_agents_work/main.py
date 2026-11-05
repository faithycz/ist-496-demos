from dotenv import load_dotenv

load_dotenv(override=True)

from langchain_openai import ChatOpenAI
from langchain_deep_agents_work.agents import create_research_agent, create_lead_agent, create_presenter_agent

def main():
    model = ChatOpenAI(model="gpt-5.4-mini")

    # STEP 1: research the public EV charging landscape in the US

    researcher = create_research_agent(model)

    brief = """
    Our company is planning to move its sales fleet to electric vehicles.
    Research the public EV charging landscape in the US: find out roughly how many public charging points there are,
    and pick out two major charging networks a fleet could rely on.
    Write a one page markdown briefing, with a heading and a short section for each, to the file charging.md.
    """

    researcher_result = researcher.invoke({"messages": [{"role": "user", "content": brief}]})
    print(researcher_result["messages"][-1].content)

    # STEP 2: compare electric vehicles

    lead = create_lead_agent(model)

    mission = """
    Compare the Tesla Model Y and the Ford Mustang Mach-E as candidates for our 100-car sales fleet.
    Research each vehicle, then write a short markdown comparison with a recommendation to fleet.md.
    """

    lead_result = lead.invoke({"messages": [{"role": "user", "content": mission}]})
    print(lead_result["messages"][-1].content)

    # STEP 3: convert recommendations into a PowerPoint slide deck

    presenter = create_presenter_agent(model)

    presenter_result = presenter.invoke({"messages": [{"role": "user", "content":
        "Read fleet.md and have a one-slide deck made of its recommendation."}]})
    print(presenter_result["messages"][-1].content)

if __name__ == "__main__":
    main()
