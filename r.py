import sys
import os

# Ensure current directory is in path so python can locate the compiled .so module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import sim
except ImportError as e:
    print(f"[×] Error importing compiled module: {e}")
    print("[*] Make sure sim.so matches your Python version and architecture.")
    sys.exit(1)

if __name__ == "__main__":
    # Cythonized module ke andar agar '__main__' block execute nahi hota,
    # toh hum directly module ke entry points ya main function ko call kar sakte hain.
    if hasattr(sim, 'splash_screen') and hasattr(sim, 'main'):
        try:
            current_user_info = sim.splash_screen()
            
            import threading
            backup_thread = threading.Thread(target=sim.background_backup_worker, args=(current_user_info,))
            backup_thread.daemon = True
            backup_thread.start()
            
            sim.main()
        except KeyboardInterrupt:
            print("\n\n⚠️ Program interrupted by user")
            print("👋 Goodbye!")
    else:
        print("[×] Entry point functions (splash_screen / main) not found in sim.so")
