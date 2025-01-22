import os
import uuid
import streamlit as st
from dotenv import load_dotenv
from client.client import AgentClient, AgentClientError

# Load product catalog
PRODUCT_CATALOG = [
    {
        "product_name": "Gala Apples",
        "description": "Sweet and crisp Gala apples, perfect for snacking.",
        "category": "Produce",
        "price": 1.99,
        "quantity": 100
    },
    {
        "product_name": "Ripe Bananas",
        "description": "Fresh, ripe bananas, a good source of potassium.",
        "category": "Produce",
        "price": 0.50,
        "quantity": 50
    },
    {
        "product_name": "Navel Oranges",
        "description": "Juicy and seedless Navel oranges, rich in Vitamin C.",
        "category": "Produce",
        "price": 0.75,
        "quantity": 75
    },
    {
        "product_name": "Strawberries",
        "description": "Sweet and juicy strawberries, perfect for desserts and snacks.",
        "category": "Produce",
        "price": 3.99,
        "quantity": 60
    },
    {
        "product_name": "Avocados",
        "description": "Creamy and nutritious avocados, a good source of healthy fats.",
        "category": "Produce",
        "price": 1.50,
        "quantity": 40
    },
    {
        "product_name": "Red Grapes",
        "description": "Sweet and crisp red grapes, perfect for snacking.",
        "category": "Produce",
        "price": 2.99,
        "quantity": 30
    },
    {
        "product_name": "Blueberries",
        "description": "Fresh blueberries, packed with antioxidants.",
        "category": "Produce",
        "price": 4.99,
        "quantity": 80
    },
    {
        "product_name": "Lemons",
        "description": "Tart and juicy lemons, perfect for cooking and drinks.",
        "category": "Produce",
        "price": 0.60,
        "quantity": 90
    },
    {
        "product_name": "Watermelon",
        "description": "Sweet and refreshing watermelon, perfect for summer.",
        "category": "Produce",
        "price": 5.99,
        "quantity": 55
    },
    {
        "product_name": "Pineapple",
        "description": "Tropical pineapple, sweet and juicy.",
        "category": "Produce",
        "price": 3.50,
        "quantity": 65
    }
]

async def main():
    # Page config
    st.set_page_config(
        page_title="AI Shopping Assistant",
        page_icon="🛒",
        layout="wide"
    )

    # Custom CSS for styling
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Center chat container */
        .stChatFloatingInputContainer {
            max-width: 800px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        
        /* Style message containers */
        .stChatMessage {
            background-color: #f0f2f6;
            border-radius: 15px;
            padding: 10px;
            margin: 5px 0;
        }
        
        /* Custom header styling */
        .chat-header {
            text-align: center;
            padding: 20px;
            background-color: #f8f9fa;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        /* Sidebar styling */
        .css-1d391kg {
            background-color: #f8f9fa;
        }

        /* Change message card background to grey */
        .stChatMessage div {
            background-color: #f1f1f1 !important;
        }
        
        /* Ensure text is visible on grey background */
        .stChatMessage p {
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "customer_id" not in st.session_state:
        st.session_state.customer_id = str(uuid.uuid4())
    if "agent_client" not in st.session_state:
        load_dotenv()
        agent_url = os.getenv("AGENT_URL", "http://localhost:8000")
        st.session_state.agent_client = AgentClient(base_url=agent_url)
    if "memory" not in st.session_state:
        st.session_state.memory = {}

    # Create sidebar
    with st.sidebar:
        st.title("🤖 AI Assistant")
        st.markdown("---")
        
        # Product Catalog Button
        if st.button("📦 View Product Catalog"):
            st.session_state.show_products = True
        
        # Schedule Meeting Button
        if st.button("📅 Schedule Meeting"):
            st.session_state.show_scheduler = True
            
        # Memory System Status
        st.markdown("### 🧠 Memory System")
        st.write(f"Conversation ID: {st.session_state.customer_id[:8]}...")
        
        st.markdown("---")
        st.markdown("### Assistant Capabilities")
        st.markdown("""
        - Product recommendations
        - Meeting scheduling
        - Personalized assistance
        - Order history tracking
        """)

    # Main chat container
    st.markdown("<div class='chat-header'>", unsafe_allow_html=True)
    st.title("💬 AI Shopping Assistant")
    st.markdown("Your personal shopping and scheduling companion")
    st.markdown("</div>", unsafe_allow_html=True)

    # Display product catalog modal
    if "show_products" in st.session_state and st.session_state.show_products:
        with st.expander("Product Catalog", expanded=True):
            cols = st.columns(3)
            for i, product in enumerate(PRODUCT_CATALOG):
                with cols[i % 3]:
                    st.markdown(f"""
                    **{product['product_name']}**  
                    {product['description']}  
                    💰 ${product['price']:.2f}  
                    📦 Stock: {product['quantity']}
                    """)
            if st.button("Close Catalog"):
                st.session_state.show_products = False
                st.rerun()

    # Display existing messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🤖" if message["role"] == "ai" else "👤"):
            st.write(message["content"])

    # Handle user input
    if user_input := st.chat_input("How can I help you today?"):
        # Display user message
        with st.chat_message("human", avatar="👤"):
            st.write(user_input)
        st.session_state.messages.append({"role": "human", "content": user_input})

        # Get AI response
        try:
            with st.spinner("Thinking..."):
                response = await st.session_state.agent_client.ainvoke(
                    content=user_input,
                    customer_id=st.session_state.customer_id
                )
            
            # Display AI response
            with st.chat_message("ai", avatar="🤖"):
                st.write(response.content)
            st.session_state.messages.append({"role": "ai", "content": response.content})

        except AgentClientError as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())