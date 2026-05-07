from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

load_dotenv()

# Define the agent state
class AgentState(TypedDict):
    """State for the LangGraph agent."""
    messages: List[Dict[str, Any]]
    context: Dict[str, Any]
    task_completed: bool
    response: Optional[str]

class LangGraphAgent:
    """A LangGraph-powered AI agent with multi-step reasoning.
    
    Supports multiple LLM providers:
    - OpenAI (default)
    - OpenRouter (with any model)
    - Anthropic (Claude)
    """
    
    def __init__(self, provider="openai", model_name=None):
        """
        Initialize the agent with a specific provider and model.
        
        Args:
            provider: "openai", "openrouter", or "anthropic"
            model_name: Model identifier (e.g., "gpt-4o-mini", "anthropic/claude-3.5-sonnet")
        """
        self.provider = provider
        
        if provider == "openai":
            self.llm = ChatOpenAI(
                model=model_name or "gpt-4o-mini",
                temperature=0.7,
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif provider == "openrouter":
            # OpenRouter uses the OpenAI-compatible API format
            # Models are specified as "provider/model-name"
            self.llm = ChatOpenAI(
                model=model_name or "meta-llama/llama-3.1-8b-instruct",
                temperature=0.7,
                openai_api_key=os.getenv("OPENROUTER_API_KEY"),
                openai_api_base="https://openrouter.ai/api/v1",
                default_headers={
                    "HTTP-Referer": "https://github.com/vsc100/langgraph-copilotkit-agent",
                    "X-Title": "LangGraph CopilotKit Agent"
                }
            )
        elif provider == "anthropic":
            self.llm = ChatAnthropic(
                model=model_name or "claude-3.5-sonnet-20241022",
                temperature=0.7,
                api_key=os.getenv("ANTHROPIC_API_KEY")
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}. Use 'openai', 'openrouter', or 'anthropic'.")
        
        self.graph = self._build_graph()
        self.thread_id = "default"
        print(f"✅ Agent initialized with {provider}: {self.llm.model_name}")
    def analyze_input(self, state: AgentState) -> Dict[str, Any]:
        """Analyze user input and extract intent."""
        messages = state["messages"]
        
        system_prompt = """You are an analysis assistant. Analyze the user's input and determine:
        1. The main intent/request
        2. Key entities or topics mentioned
        3. Complexity level (simple, moderate, complex)
        4. Recommended approach
        
        Provide a structured analysis in JSON format."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Analyze this request: {input}")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            last_message = messages[-1] if messages else {"content": "No input"}
            input_text = last_message.get("content", "No input")
            analysis = chain.invoke({"input": input_text})
            
            return {
                "context": {
                    **state["context"],
                    "analysis": analysis,
                    "stage": "analyzed"
                }
            }
        except Exception as e:
            return {
                "context": {
                    **state["context"],
                    "error": str(e),
                    "stage": "error"
                }
            }
    
    def plan_action(self, state: AgentState) -> Dict[str, Any]:
        """Plan the actions to take based on analysis."""
        context = state["context"]
        messages = state["messages"]
        
        system_prompt = """You are a planning assistant. Based on the analysis and conversation history,
        create a step-by-step plan to address the user's request.
        
        Provide your plan as a numbered list of clear, actionable steps."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Messages: {messages}\n\nAnalysis: {analysis}\n\nCreate a plan:")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            analysis = context.get("analysis", "No analysis available")
            
            plan = chain.invoke({
                "messages": str([m.get("content", "") for m in messages]),
                "analysis": analysis
            })
            
            return {
                "context": {
                    **context,
                    "plan": plan,
                    "stage": "planned"
                }
            }
        except Exception as e:
            return {
                "context": {
                    **context,
                    "error": str(e),
                    "stage": "error"
                }
            }
    
    def execute_action(self, state: AgentState) -> Dict[str, Any]:
        """Execute the planned actions."""
        context = state["context"]
        messages = state["messages"]
        
        system_prompt = """You are an execution assistant. Execute the plan to address the user's request.
        Use the conversation context and the plan to generate a comprehensive response.
        
        Be helpful, clear, and provide detailed explanations."""
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Messages: {messages}\n\nPlan: {plan}\n\nExecute and respond:")
        ])
        
        chain = prompt | self.llm | StrOutputParser()
        
        try:
            plan = context.get("plan", "No plan available")
            
            response = chain.invoke({
                "messages": str([m.get("content", "") for m in messages]),
                "plan": plan
            })
            
            return {
                "context": {
                    **context,
                    "stage": "executed"
                },
                "response": response
            }
        except Exception as e:
            return {
                "context": {
                    **context,
                    "error": str(e),
                    "stage": "error"
                },
                "response": f"Error during execution: {str(e)}"
            }
    
    def generate_response(self, state: AgentState) -> Dict[str, Any]:
        """Generate the final response."""
        response = state.get("response", "I apologize, but I couldn't generate a response.")
        context = state["context"]
        
        return {
            "response": response,
            "context": {
                **context,
                "stage": "completed",
                "task_completed": True
            },
            "task_completed": True
        }
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("analyze", self.analyze_input)
        workflow.add_node("plan", self.plan_action)
        workflow.add_node("execute", self.execute_action)
        workflow.add_node("respond", self.generate_response)
        
        # Add edges
        workflow.add_edge("analyze", "plan")
        workflow.add_edge("plan", "execute")
        workflow.add_edge("execute", "respond")
        
        # Set entry point
        workflow.set_entry_point("analyze")
        
        return workflow.compile()
    
    async def arun(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run the agent asynchronously."""
        state = AgentState(
            messages=messages,
            context={"stage": "initial"},
            task_completed=False,
            response=None
        )
        
        try:
            result = await self.graph.ainvoke(state)
            return result
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "context": {"stage": "error", "error": str(e)},
                "task_completed": False
            }
    
    def run(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Run the agent synchronously."""
        state = AgentState(
            messages=messages,
            context={"stage": "initial"},
            task_completed=False,
            response=None
        )
        
        try:
            result = self.graph.invoke(state)
            return result
        except Exception as e:
            return {
                "response": f"Error: {str(e)}",
                "context": {"stage": "error", "error": str(e)},
                "task_completed": False
            }
