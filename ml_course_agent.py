#!/usr/bin/env python3
"""
ML Course Agent - An Interactive Assistant for Machine Learning for Beginners Course

This agent helps students navigate the ML curriculum, provides information about lessons,
tracks progress, and offers interactive guidance throughout the learning journey.
"""

import json
import os
import sys
from datetime import datetime
from typing import Dict, List, Optional


class MLCourseAgent:
    """An intelligent agent to assist with the ML for Beginners curriculum."""
    
    def __init__(self):
        self.course_structure = self._load_course_structure()
        self.user_progress = {}
        self.current_lesson = None
        
    def _load_course_structure(self) -> Dict:
        """Load the course structure with all lessons and topics."""
        return {
            "1-Introduction": {
                "title": "Introduction to Machine Learning",
                "lessons": [
                    {"num": 1, "title": "Introduction to machine learning", "path": "1-Introduction/1-intro-to-ML"},
                    {"num": 2, "title": "The History of machine learning", "path": "1-Introduction/2-history-of-ML"},
                    {"num": 3, "title": "Fairness and machine learning", "path": "1-Introduction/3-fairness"},
                    {"num": 4, "title": "Techniques for machine learning", "path": "1-Introduction/4-techniques-of-ML"}
                ]
            },
            "2-Regression": {
                "title": "Regression",
                "lessons": [
                    {"num": 5, "title": "Introduction to regression", "path": "2-Regression/1-Tools"},
                    {"num": 6, "title": "North American pumpkin prices (Data preparation)", "path": "2-Regression/2-Data"},
                    {"num": 7, "title": "North American pumpkin prices (Linear & Polynomial)", "path": "2-Regression/3-Linear"},
                    {"num": 8, "title": "North American pumpkin prices (Logistic)", "path": "2-Regression/4-Logistic"}
                ]
            },
            "3-Web-App": {
                "title": "Build a Web Application",
                "lessons": [
                    {"num": 9, "title": "Build a web app to use your ML model", "path": "3-Web-App/1-Web-App"}
                ]
            },
            "4-Classification": {
                "title": "Classification",
                "lessons": [
                    {"num": 10, "title": "Introduction to classification", "path": "4-Classification/1-Introduction"},
                    {"num": 11, "title": "Delicious Asian and Indian cuisines", "path": "4-Classification/2-Classifiers-1"},
                    {"num": 12, "title": "More delicious Asian cuisines", "path": "4-Classification/3-Classifiers-2"},
                    {"num": 13, "title": "Build a recommender system", "path": "4-Classification/4-Applied"}
                ]
            },
            "5-Clustering": {
                "title": "Clustering",
                "lessons": [
                    {"num": 14, "title": "Introduction to clustering", "path": "5-Clustering/1-Visualize"},
                    {"num": 15, "title": "Exploring Nigerian Musical Tastes", "path": "5-Clustering/2-K-Means"}
                ]
            },
            "6-NLP": {
                "title": "Natural Language Processing",
                "lessons": [
                    {"num": 16, "title": "Introduction to NLP", "path": "6-NLP/1-Introduction-to-NLP"},
                    {"num": 17, "title": "Common NLP Tasks", "path": "6-NLP/2-Tasks"},
                    {"num": 18, "title": "Translation and sentiment analysis", "path": "6-NLP/3-Translation-Sentiment"},
                    {"num": 19, "title": "Romantic hotels of Europe (Sentiment)", "path": "6-NLP/4-Hotel-Reviews-1"},
                    {"num": 20, "title": "Romantic hotels of Europe (Embeddings)", "path": "6-NLP/5-Hotel-Reviews-2"}
                ]
            },
            "7-TimeSeries": {
                "title": "Time Series",
                "lessons": [
                    {"num": 21, "title": "Introduction to time series forecasting", "path": "7-TimeSeries/1-Introduction"},
                    {"num": 22, "title": "ARIMA models", "path": "7-TimeSeries/2-ARIMA"}
                ]
            },
            "8-Reinforcement": {
                "title": "Reinforcement Learning",
                "lessons": [
                    {"num": 23, "title": "Introduction to reinforcement learning", "path": "8-Reinforcement/1-QLearning"},
                    {"num": 24, "title": "Help Peter avoid the wolf! (Q-Learning)", "path": "8-Reinforcement/2-Gym"}
                ]
            },
            "9-Real-World": {
                "title": "Real-World ML Applications",
                "lessons": [
                    {"num": 25, "title": "Real-world ML applications and scenarios", "path": "9-Real-World/1-Applications"}
                ]
            }
        }
    
    def welcome(self):
        """Display welcome message."""
        print("=" * 70)
        print("🤖 Welcome to the ML for Beginners Course Agent!")
        print("=" * 70)
        print("\nI'm your interactive assistant for the Machine Learning curriculum.")
        print("I can help you with:")
        print("  • Navigate through 26 lessons across 9 major topics")
        print("  • Get information about specific lessons")
        print("  • Track your learning progress")
        print("  • Find resources and prerequisites")
        print("  • Answer questions about the course structure")
        print("\nType 'help' to see available commands or 'quit' to exit.")
        print("=" * 70)
    
    def show_help(self):
        """Display available commands."""
        print("\n📚 Available Commands:")
        print("-" * 70)
        print("  list              - Show all course topics and lessons")
        print("  lesson <num>      - Get details about a specific lesson (e.g., 'lesson 5')")
        print("  topic <name>      - Show all lessons in a topic (e.g., 'topic regression')")
        print("  search <keyword>  - Search for lessons by keyword")
        print("  progress          - View your learning progress")
        print("  mark <num>        - Mark a lesson as completed (e.g., 'mark 5')")
        print("  recommend         - Get a lesson recommendation based on progress")
        print("  quiz              - Get information about quizzes")
        print("  resources         - Show additional learning resources")
        print("  help              - Show this help message")
        print("  quit              - Exit the agent")
        print("-" * 70)
    
    def list_courses(self):
        """List all course topics and lessons."""
        print("\n📖 Course Structure (26 Lessons):")
        print("=" * 70)
        for section_key, section in self.course_structure.items():
            print(f"\n{section['title']}")
            print("-" * 70)
            for lesson in section['lessons']:
                status = "✓" if self.user_progress.get(lesson['num'], False) else " "
                print(f"  [{status}] Lesson {lesson['num']:2d}: {lesson['title']}")
        print("=" * 70)
    
    def get_lesson_details(self, lesson_num: int):
        """Get detailed information about a specific lesson."""
        for section in self.course_structure.values():
            for lesson in section['lessons']:
                if lesson['num'] == lesson_num:
                    completed = self.user_progress.get(lesson_num, False)
                    status = "✓ Completed" if completed else "⏳ Not Started"
                    
                    print(f"\n📚 Lesson {lesson_num}: {lesson['title']}")
                    print("=" * 70)
                    print(f"Status: {status}")
                    print(f"Section: {section['title']}")
                    print(f"Path: {lesson['path']}/README.md")
                    print("\nWhat to expect:")
                    print("  • Pre-lecture warmup quiz")
                    print("  • Written lesson with examples")
                    print("  • Hands-on project or exercises")
                    print("  • Knowledge checks")
                    print("  • Post-lecture quiz")
                    print("  • Assignment")
                    print(f"\n💡 Tip: Navigate to '{lesson['path']}' to start the lesson!")
                    print("=" * 70)
                    return
        
        print(f"\n❌ Lesson {lesson_num} not found. Please use a number between 1-26.")
    
    def get_topic_lessons(self, topic_name: str):
        """Get all lessons for a specific topic."""
        topic_name = topic_name.lower().strip()
        
        # Map common names to section keys
        topic_map = {
            'intro': '1-Introduction',
            'introduction': '1-Introduction',
            'regression': '2-Regression',
            'web': '3-Web-App',
            'webapp': '3-Web-App',
            'classification': '4-Classification',
            'clustering': '5-Clustering',
            'nlp': '6-NLP',
            'timeseries': '7-TimeSeries',
            'time': '7-TimeSeries',
            'reinforcement': '8-Reinforcement',
            'rl': '8-Reinforcement',
            'real': '9-Real-World',
            'applications': '9-Real-World'
        }
        
        section_key = topic_map.get(topic_name)
        if not section_key:
            print(f"\n❌ Topic '{topic_name}' not found.")
            print("Available topics: introduction, regression, web, classification, clustering, nlp, timeseries, reinforcement, real-world")
            return
        
        section = self.course_structure[section_key]
        print(f"\n📖 {section['title']}")
        print("=" * 70)
        for lesson in section['lessons']:
            status = "✓" if self.user_progress.get(lesson['num'], False) else " "
            print(f"  [{status}] Lesson {lesson['num']:2d}: {lesson['title']}")
        print("=" * 70)
    
    def search_lessons(self, keyword: str):
        """Search for lessons by keyword."""
        keyword = keyword.lower().strip()
        results = []
        
        for section in self.course_structure.values():
            for lesson in section['lessons']:
                if keyword in lesson['title'].lower() or keyword in section['title'].lower():
                    results.append((section['title'], lesson))
        
        if results:
            print(f"\n🔍 Search results for '{keyword}':")
            print("=" * 70)
            for section_title, lesson in results:
                status = "✓" if self.user_progress.get(lesson['num'], False) else " "
                print(f"  [{status}] Lesson {lesson['num']:2d}: {lesson['title']}")
                print(f"      Section: {section_title}")
            print("=" * 70)
        else:
            print(f"\n❌ No lessons found matching '{keyword}'")
    
    def show_progress(self):
        """Show user's learning progress."""
        total_lessons = sum(len(section['lessons']) for section in self.course_structure.values())
        completed = sum(1 for status in self.user_progress.values() if status)
        percentage = (completed / total_lessons * 100) if total_lessons > 0 else 0
        
        print("\n📊 Your Learning Progress")
        print("=" * 70)
        print(f"Completed: {completed}/{total_lessons} lessons ({percentage:.1f}%)")
        print(f"Progress: [{'█' * int(percentage/5)}{'░' * (20-int(percentage/5))}] {percentage:.1f}%")
        
        if completed > 0:
            print("\n✓ Completed Lessons:")
            for lesson_num in sorted([k for k, v in self.user_progress.items() if v]):
                for section in self.course_structure.values():
                    for lesson in section['lessons']:
                        if lesson['num'] == lesson_num:
                            print(f"  • Lesson {lesson_num}: {lesson['title']}")
        
        if completed < total_lessons:
            print("\n⏳ Remaining Lessons:")
            remaining = []
            for section in self.course_structure.values():
                for lesson in section['lessons']:
                    if not self.user_progress.get(lesson['num'], False):
                        remaining.append(lesson['num'])
            print(f"  {len(remaining)} lessons to go!")
        
        print("=" * 70)
    
    def mark_completed(self, lesson_num: int):
        """Mark a lesson as completed."""
        # Validate lesson number
        valid = False
        for section in self.course_structure.values():
            for lesson in section['lessons']:
                if lesson['num'] == lesson_num:
                    valid = True
                    break
        
        if valid:
            self.user_progress[lesson_num] = True
            print(f"\n✓ Lesson {lesson_num} marked as completed! Keep up the great work! 🎉")
            self._save_progress()
        else:
            print(f"\n❌ Lesson {lesson_num} not found. Please use a number between 1-26.")
    
    def recommend_lesson(self):
        """Recommend next lesson based on progress."""
        # Find the first incomplete lesson
        for section in self.course_structure.values():
            for lesson in section['lessons']:
                if not self.user_progress.get(lesson['num'], False):
                    print(f"\n💡 Recommended Next Lesson:")
                    print("=" * 70)
                    print(f"Lesson {lesson['num']}: {lesson['title']}")
                    print(f"Section: {section['title']}")
                    print(f"Path: {lesson['path']}/README.md")
                    print("\nThis lesson follows the natural progression of the curriculum.")
                    print("=" * 70)
                    return
        
        print("\n🎉 Congratulations! You've completed all lessons!")
    
    def show_quiz_info(self):
        """Show information about quizzes."""
        print("\n📝 Quiz Information")
        print("=" * 70)
        print("The course includes 52 quizzes (pre- and post-lecture quizzes).")
        print("\nQuiz Features:")
        print("  • Each quiz contains 3 questions")
        print("  • Pre-lecture quizzes prepare you for the lesson")
        print("  • Post-lecture quizzes test your understanding")
        print("  • Interactive quiz app available in /quiz-app folder")
        print("\nTo use the quiz app locally:")
        print("  1. cd quiz-app")
        print("  2. npm install")
        print("  3. npm run serve")
        print("\nQuizzes are also available online at: https://aka.ms/ml-beginners")
        print("=" * 70)
    
    def show_resources(self):
        """Show additional learning resources."""
        print("\n📚 Additional Resources")
        print("=" * 70)
        print("Microsoft Learn Collections:")
        print("  • Main collection: https://learn.microsoft.com/collections/qrqzamz1nn2wx3")
        print("\nVideo Resources:")
        print("  • ML for Beginners Playlist: https://aka.ms/ml-beginners-videos")
        print("  • Course overview video available in README")
        print("\nRelated Curricula:")
        print("  • Data Science for Beginners: https://aka.ms/ds4beginners")
        print("  • AI for Beginners: https://aka.ms/ai4beginners")
        print("\nCommunity:")
        print("  • Discussion Board: GitHub Discussions")
        print("  • GitHub Issues: Report bugs or request features")
        print("\nTools & Libraries:")
        print("  • Python, Scikit-learn, Pandas, Matplotlib")
        print("  • R available for some lessons")
        print("  • Jupyter Notebooks included")
        print("=" * 70)
    
    def _save_progress(self):
        """Save progress to a JSON file."""
        try:
            progress_file = os.path.join(os.path.dirname(__file__), '.ml_agent_progress.json')
            with open(progress_file, 'w') as f:
                json.dump({
                    'progress': self.user_progress,
                    'last_updated': datetime.now().isoformat()
                }, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Could not save progress: {e}")
    
    def _load_progress(self):
        """Load progress from JSON file."""
        try:
            progress_file = os.path.join(os.path.dirname(__file__), '.ml_agent_progress.json')
            if os.path.exists(progress_file):
                with open(progress_file, 'r') as f:
                    data = json.load(f)
                    # Convert string keys back to integers
                    self.user_progress = {int(k): v for k, v in data.get('progress', {}).items()}
                    print(f"✓ Progress loaded from {data.get('last_updated', 'unknown date')}")
        except Exception as e:
            print(f"⚠️ Warning: Could not load progress: {e}")
    
    def process_command(self, command: str):
        """Process user commands."""
        command = command.strip().lower()
        parts = command.split(maxsplit=1)
        
        if not parts:
            return True
        
        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else ""
        
        if cmd in ['quit', 'exit', 'bye']:
            print("\n👋 Thank you for using the ML Course Agent! Happy learning!")
            return False
        
        elif cmd == 'help':
            self.show_help()
        
        elif cmd == 'list':
            self.list_courses()
        
        elif cmd == 'lesson':
            if arg.isdigit():
                self.get_lesson_details(int(arg))
            else:
                print("❌ Please provide a lesson number (e.g., 'lesson 5')")
        
        elif cmd == 'topic':
            if arg:
                self.get_topic_lessons(arg)
            else:
                print("❌ Please provide a topic name (e.g., 'topic regression')")
        
        elif cmd == 'search':
            if arg:
                self.search_lessons(arg)
            else:
                print("❌ Please provide a search keyword (e.g., 'search pumpkin')")
        
        elif cmd == 'progress':
            self.show_progress()
        
        elif cmd == 'mark':
            if arg.isdigit():
                self.mark_completed(int(arg))
            else:
                print("❌ Please provide a lesson number (e.g., 'mark 5')")
        
        elif cmd == 'recommend':
            self.recommend_lesson()
        
        elif cmd == 'quiz':
            self.show_quiz_info()
        
        elif cmd == 'resources':
            self.show_resources()
        
        else:
            print(f"❌ Unknown command: '{cmd}'. Type 'help' for available commands.")
        
        return True
    
    def run(self):
        """Main agent loop."""
        self._load_progress()
        self.welcome()
        
        while True:
            try:
                print("\n> ", end="")
                user_input = input()
                
                if not self.process_command(user_input):
                    break
                    
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("Please try again or type 'help' for available commands.")


def main():
    """Entry point for the ML Course Agent."""
    agent = MLCourseAgent()
    agent.run()


if __name__ == "__main__":
    main()
