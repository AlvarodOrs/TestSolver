"""
Web Automation Framework
Main entry point for web automation tasks
"""

from dotenv import load_dotenv
from bot_launcher import launch_bot
import workers
import os

# Load environment variables (override=True ensures .env values override system variables)
load_dotenv(override=True)


def main():
    """Main function to orchestrate bot operations"""
    # Launch the bot
    print("[+] Launching bot...")
    automation = launch_bot(headless=False)
    
    try:
        # Step 1: Login
        print("\n=== Step 1: Logging in ===")
        mode_login = os.getenv("AUTOMATED_LOGIN").lower() in ("true", "1", "yes")
        login_success = workers.logIn(automation, automated_login=mode_login)
        
        if not login_success:
            print("Login failed. Exiting...")
            return
        
        # Step 2: Navigate to target page (if needed)
        target_url = os.getenv("TARGET_URL")
        if target_url:
            print(f"\n=== Step 2: Navigating to target page ===")
            automation.navigate(target_url)
        
        # Step 3: Find and click on courses
        print("\n=== Step 3: Finding and clicking on courses ===")
        
        # Find and click on courses in the navigation menu
        course_data = workers.find_and_click_courses(automation)
        
        if course_data:
            # Save course data
            workers.save_course_data(course_data, "courses_data.json")
        else:
            print("Failed to find courses or no courses found.")
        
        print("\n=== Automation completed successfully! ===")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        automation.custom_close()
        print("\nBot closed.")


if __name__ == "__main__":
    main()
