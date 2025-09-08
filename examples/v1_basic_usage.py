#!/usr/bin/env python3
"""
Bob v1 Basic - Usage Examples
Demonstrates how to interact with Bob's CLI version
"""

import sys
from pathlib import Path

# Add Bob to path
sys.path.insert(0, str(Path(__file__).parent.parent / "versions" / "v1-basic"))

from bob_clean import BobBrain

def example_basic_conversation():
    """Basic conversation with Bob"""
    print("=" * 50)
    print("Example 1: Basic Conversation")
    print("=" * 50)
    
    bob = BobBrain()
    
    # Simple greeting
    response = bob.chat("Hello Bob!")
    print(f"You: Hello Bob!")
    print(f"Bob: {response}\n")
    
    # Ask about capabilities
    response = bob.chat("What can you help me with?")
    print(f"You: What can you help me with?")
    print(f"Bob: {response}\n")

def example_commands():
    """Demonstrate Bob's command system"""
    print("=" * 50)
    print("Example 2: Command System")
    print("=" * 50)
    
    bob = BobBrain()
    
    # Status command
    print("Command: status")
    response = bob.chat("status")
    print(f"Bob: {response}\n")
    
    # Memory command
    print("Command: memory")
    response = bob.chat("memory")
    print(f"Bob: {response}\n")
    
    # Project command
    print("Command: project")
    response = bob.chat("project")
    print(f"Bob: {response}\n")

def example_knowledge_query():
    """Query Bob's knowledge base"""
    print("=" * 50)
    print("Example 3: Knowledge Base Query")
    print("=" * 50)
    
    bob = BobBrain()
    
    # DiagnosticPro related query
    queries = [
        "Tell me about DiagnosticPro",
        "What is vehicle diagnostics?",
        "How can Bob help with business strategy?"
    ]
    
    for query in queries:
        print(f"You: {query}")
        response = bob.chat(query)
        print(f"Bob: {response[:200]}...\n")  # Truncate long responses

def example_conversation_flow():
    """Demonstrate a full conversation flow"""
    print("=" * 50)
    print("Example 4: Full Conversation Flow")
    print("=" * 50)
    
    bob = BobBrain()
    
    conversation = [
        "Hello Bob, I need help with my automotive repair shop",
        "We're having issues with customer trust",
        "How can DiagnosticPro help us?",
        "What about pricing transparency?",
        "Thank you for your help!"
    ]
    
    for message in conversation:
        print(f"You: {message}")
        response = bob.chat(message)
        print(f"Bob: {response[:200]}...\n")

def example_custom_integration():
    """Show how to integrate Bob into custom applications"""
    print("=" * 50)
    print("Example 5: Custom Integration")
    print("=" * 50)
    
    class CustomApp:
        def __init__(self):
            self.bob = BobBrain()
            self.conversation_history = []
        
        def process_user_input(self, user_input):
            """Process input and maintain history"""
            response = self.bob.chat(user_input)
            
            self.conversation_history.append({
                'user': user_input,
                'bob': response,
                'timestamp': 'now'
            })
            
            return response
        
        def get_history(self):
            """Get conversation history"""
            return self.conversation_history
    
    # Use custom app
    app = CustomApp()
    
    print("Custom App Integration:")
    response = app.process_user_input("Hello from custom app!")
    print(f"Response: {response}")
    
    response = app.process_user_input("Tell me about your capabilities")
    print(f"Response: {response[:100]}...")
    
    print(f"\nConversation history: {len(app.get_history())} messages")

def main():
    """Run all examples"""
    print("\n🤖 Bob v1 Basic - Usage Examples\n")
    
    examples = [
        ("Basic Conversation", example_basic_conversation),
        ("Command System", example_commands),
        ("Knowledge Query", example_knowledge_query),
        ("Conversation Flow", example_conversation_flow),
        ("Custom Integration", example_custom_integration)
    ]
    
    print("Available Examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    choice = input("\nSelect example (1-5) or 'all' for all examples: ").strip()
    
    if choice == 'all':
        for name, func in examples:
            func()
            input("\nPress Enter to continue...")
    elif choice.isdigit() and 1 <= int(choice) <= len(examples):
        examples[int(choice) - 1][1]()
    else:
        print("Invalid choice. Running basic conversation example...")
        example_basic_conversation()

if __name__ == "__main__":
    main()