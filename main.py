from engine import handle_turn

if __name__ == "__main__":
    try:
        from engine import handle_turn
        print("✓ engine import OK")
    except Exception as e:
        print(f"✗ engine import failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    print("PDA32D CLI – type 'quit' om te stoppen.\n")
    session_id = "cli"

    while True:
        user_text = input("you> ").strip()
        if user_text.lower() in {"quit", "exit"}:
            break

        result = handle_turn(session_id, user_text)
        print(f"pda> {result['assistant_text']}")


if __name__ == "__main__":
    main()

def main():
    print("PDA32D CLI – type 'quit' om te stoppen, 'memory' om geschiedenis te zien.\n")
    session_id = "cli"
    
    while True:
        user_text = input("you> ").strip()
        if user_text.lower() in {"quit", "exit"}:
            break
        
        # Debug command
        if user_text.lower() == "memory":
            from core.memory import get_session_memory
            mem = get_session_memory(session_id)
            print(f"\n[Memory: {len(mem.turns)} turns]")
            for turn in mem.turns[-5:]:  # laatste 5
                role = "YOU" if turn.role == "user" else "PDA"
                print(f"  {role}: {turn.text[:60]}...")
            print()
            continue
        
        result = handle_turn(session_id, user_text)
        print(f"pda> {result['assistant_text']}")