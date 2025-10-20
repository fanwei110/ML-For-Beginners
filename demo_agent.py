#!/usr/bin/env python3
"""
Quick Start Demo for ML Course Agent

This script demonstrates the key features of the ML Course Agent
with a pre-scripted interactive session.
"""

import sys
import time
from ml_course_agent import MLCourseAgent


def print_section(title):
    """Print a section separator."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def simulate_command(agent, command, delay=1.5):
    """Simulate a user command with a short delay."""
    print(f"\n> {command}")
    time.sleep(delay)
    agent.process_command(command)
    time.sleep(delay)


def run_demo():
    """Run a demonstration of the ML Course Agent features."""
    print_section("ML COURSE AGENT - QUICK START DEMO")
    print("\nThis demo showcases the main features of the agent.")
    print("Press Ctrl+C at any time to exit.")
    time.sleep(2)
    
    # Initialize agent
    agent = MLCourseAgent()
    agent.welcome()
    
    # Demo 1: Show help
    print_section("DEMO 1: Getting Help")
    print("Let's start by viewing all available commands...")
    simulate_command(agent, "help")
    
    # Demo 2: List courses
    print_section("DEMO 2: Browsing Course Structure")
    print("Now let's see all 26 lessons in the curriculum...")
    simulate_command(agent, "list")
    
    # Demo 3: View lesson details
    print_section("DEMO 3: Exploring a Specific Lesson")
    print("Let's get details about Lesson 5 (Introduction to Regression)...")
    simulate_command(agent, "lesson 5")
    
    # Demo 4: Search functionality
    print_section("DEMO 4: Searching for Topics")
    print("Searching for lessons about 'NLP'...")
    simulate_command(agent, "search nlp")
    
    # Demo 5: Topic browsing
    print_section("DEMO 5: Browsing by Topic")
    print("Let's view all lessons in the Classification topic...")
    simulate_command(agent, "topic classification")
    
    # Demo 6: Mark progress
    print_section("DEMO 6: Tracking Progress")
    print("Let's mark a few lessons as completed...")
    simulate_command(agent, "mark 1", 1)
    simulate_command(agent, "mark 5", 1)
    simulate_command(agent, "mark 10", 1)
    
    # Demo 7: View progress
    print_section("DEMO 7: Viewing Your Progress")
    print("Now let's check our learning progress...")
    simulate_command(agent, "progress")
    
    # Demo 8: Get recommendation
    print_section("DEMO 8: Getting Recommendations")
    print("The agent can recommend your next lesson...")
    simulate_command(agent, "recommend")
    
    # Demo 9: Quiz information
    print_section("DEMO 9: Quiz Information")
    print("Let's learn about the course quizzes...")
    simulate_command(agent, "quiz")
    
    # Demo 10: Resources
    print_section("DEMO 10: Additional Resources")
    print("Finally, let's see what additional resources are available...")
    simulate_command(agent, "resources")
    
    # Conclusion
    print_section("DEMO COMPLETED!")
    print("\n✨ You've seen all the main features of the ML Course Agent!")
    print("\nTo use the agent interactively, run:")
    print("  python ml_course_agent.py")
    print("\nOr in Chinese (中文):")
    print("  这是一个帮助你学习机器学习课程的智能助手！")
    print("  运行命令: python ml_course_agent.py")
    print("\nHappy Learning! 🚀📚")
    print("=" * 70)


def main():
    """Main entry point for the demo."""
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
