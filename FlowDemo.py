import asyncio
from crewai import Agent, Crew, Task, LLM
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from typing import List
from litellm import completion
import sys
sys.stdout.reconfigure(encoding='utf-8')

class BlogState(BaseModel):
    topic: str = ""
    research_notes: List[str] = []
    draft_content: str = ""
    final_content: str = ""

class BlogContentFlow(Flow[BlogState]):
    
    model = LLM(
        model='ollama/llama3.2:3b',
        base_url='http://localhost:11434',
    )

    def __init__(self):
        super().__init__()

        # Définition des agents
        self.researcher = Agent(
            name="Researcher",
            role="researcher",  # Ajout du rôle obligatoire
            goal="Conduct thorough research on tech topics",
            backstory="Expert tech researcher with years of experience",
            llm=self.model,
            verbose=True,
            tools=[]
        )

        self.writer = Agent(
            name="Writer",
            role="writer",  # Ajout du rôle obligatoire
            goal="Create engaging tech content",
            backstory="Experienced tech writer and blogger",
            llm=self.model,
            verbose=True,
            tools=[]
        )

        self.editor = Agent(
            name="Editor",
            role="editor",  # Ajout du rôle obligatoire
            goal="Ensure content quality and accuracy",
            backstory="Senior content editor with technical expertise",
            llm=self.model,
            verbose=True,
            tools=[]
        )


    @start()
    def generate_topic(self):
        response = completion(
            model=self.model.model,
            messages=[{
                "role": "user",
                "content": "Generate a trending tech blog post topic for 2024."
            }]
        )
        topic = response["choices"][0]["message"]["content"]
        self.state.topic = topic
        print(f"Generated Topic: {topic}")
        return topic

    @listen(generate_topic)
    def conduct_research(self, topic):
        research_crew = Crew(
            agents=[self.researcher],
            tasks=[
                Task(
                    description=f"Research key points about: {topic}",
                    agent=self.researcher,
                    expected_output="A list of key points with sources on the topic"
                ),
                Task(
                    description="Identify relevant statistics and examples",
                    agent=self.researcher,
                    expected_output="A list of statistics and real-world examples related to the topic"
                )
            ]
        )
        
        research_results = research_crew.kickoff()
        self.state.research_notes = research_results
        print(f"Research Notes: {research_results}")
        return research_results

    @listen(conduct_research)
    def write_content(self, research):
        writing_crew = Crew(
            agents=[self.writer],
            tasks=[
                Task(
                    description=f"""Write a blog post about {self.state.topic} 
                    using this research: {research}""",
                    agent=self.writer,
                    expected_output="A well-structured blog post with an engaging introduction, clear explanations, and a conclusion."
                )
            ]
        )
        
        draft = writing_crew.kickoff()
        self.state.draft_content = draft
        print(f"Draft Content: {draft}")
        return draft

    @listen(write_content)
    def edit_content(self, draft):
        editing_crew = Crew(
            agents=[self.editor],
            tasks=[
                Task(
                    description=f"Edit and improve this blog post: {draft}",
                    agent=self.editor,
                    expected_output="A polished and well-structured blog post with improved clarity, grammar, and readability."
                )
            ]
        )
        
        final_content = editing_crew.kickoff()
        self.state.final_content = final_content
        print(f"Final Content: {final_content}")
        return final_content

async def main():
    flow = BlogContentFlow()
    flow.plot()  # Visualisation du workflow
    result = await flow.kickoff_async()

    print(f"Final Blog Post:\n{result}")

if __name__ == "__main__":
    asyncio.run(main())
