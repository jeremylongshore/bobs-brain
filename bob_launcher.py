#!/usr/bin/env python3
"""
Bob's Brain Launcher - Simple startup script
"""
import sys
import asyncio
from pathlib import Path

# Add agent directory to path
sys.path.append(str(Path(__file__).parent / "agent"))


def show_banner():
    """Show Bob's Brain banner"""
    print("🧠" + "=" * 50 + "🧠")
    print("    BOB'S BRAIN - ReAct Reasoning Assistant")
    print("    Phase 3: Open Source ReAct Implementation")
    print("    Using: LangChain + Ollama + ChromaDB")
    print("🧠" + "=" * 50 + "🧠")


async def launch_bob():
    """Launch Bob with error handling"""
    show_banner()

    try:
        from bob_react_opensource import BobReActOpenSource

        print("\n🚀 Initializing Bob ReAct...")
        bob = BobReActOpenSource()

        print("\n" + bob.get_status())
        print("\n💡 Available commands: 'status', 'exit', or just chat normally")
        print("📝 Example: 'Search for DiagnosticPro information'")

        while True:
            try:
                user_input = input("\n💬 You: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("👋 Bob: Reasoning session complete!")
                    break

                if user_input.lower() == "status":
                    print(bob.get_status())
                    continue

                print("\n🤔 Bob is reasoning...")
                response = await bob.chat(user_input)
                print(f"\n🤖 Bob: {response}")

            except KeyboardInterrupt:
                print("\n👋 Bob: Shutting down reasoning engine!")
                break
            except EOFError:
                print("\n👋 Bob: Session ended!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

    except ImportError as e:
        print(f"❌ Failed to import Bob: {e}")
        print("Make sure you're in the bobs_brain directory")
    except Exception as e:
        print(f"❌ Failed to initialize Bob: {e}")
        print("Make sure Ollama is running with mistral:7b model")

if __name__ == "__main__":
    asyncio.run(launch_bob())
