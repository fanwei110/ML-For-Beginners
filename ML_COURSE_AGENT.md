# ML Course Agent 🤖

An intelligent interactive assistant designed to help students navigate and learn from the **Machine Learning for Beginners** curriculum.

## Overview

The ML Course Agent is a command-line tool that provides an interactive interface for:
- Navigating through the 26-lesson curriculum
- Tracking learning progress
- Finding specific lessons and topics
- Getting recommendations for what to learn next
- Accessing course resources and quiz information

## Features

### 🎯 Core Features

- **Course Navigation**: Browse all 26 lessons organized across 9 major topics
- **Lesson Details**: Get comprehensive information about any specific lesson
- **Progress Tracking**: Mark lessons as completed and visualize your progress
- **Smart Search**: Find lessons by keywords
- **Recommendations**: Get personalized lesson recommendations based on your progress
- **Quiz Information**: Access details about pre- and post-lecture quizzes
- **Resource Links**: Quick access to additional learning materials

### 📚 Course Structure

The agent covers all course topics:
1. **Introduction to Machine Learning** (4 lessons)
2. **Regression** (4 lessons)
3. **Build a Web Application** (1 lesson)
4. **Classification** (4 lessons)
5. **Clustering** (2 lessons)
6. **Natural Language Processing** (5 lessons)
7. **Time Series** (2 lessons)
8. **Reinforcement Learning** (2 lessons)
9. **Real-World ML Applications** (1 lesson)

## Installation

### Prerequisites

- Python 3.6 or higher
- No additional dependencies required (uses only Python standard library)

### Setup

1. The agent is already included in the repository as `ml_course_agent.py`
2. Make it executable (optional):
   ```bash
   chmod +x ml_course_agent.py
   ```

## Usage

### Starting the Agent

```bash
python ml_course_agent.py
```

Or if made executable:
```bash
./ml_course_agent.py
```

### Available Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show all available commands | `help` |
| `list` | Display all course topics and lessons | `list` |
| `lesson <num>` | Get details about a specific lesson | `lesson 5` |
| `topic <name>` | Show all lessons in a topic | `topic regression` |
| `search <keyword>` | Search for lessons by keyword | `search pumpkin` |
| `progress` | View your learning progress | `progress` |
| `mark <num>` | Mark a lesson as completed | `mark 5` |
| `recommend` | Get a lesson recommendation | `recommend` |
| `quiz` | Get information about quizzes | `quiz` |
| `resources` | Show additional learning resources | `resources` |
| `quit` | Exit the agent | `quit` |

### Example Session

```
🤖 Welcome to the ML for Beginners Course Agent!
======================================================================

I'm your interactive assistant for the Machine Learning curriculum.
I can help you with:
  • Navigate through 26 lessons across 9 major topics
  • Get information about specific lessons
  • Track your learning progress
  • Find resources and prerequisites
  • Answer questions about the course structure

Type 'help' to see available commands or 'quit' to exit.
======================================================================

> list

📖 Course Structure (26 Lessons):
======================================================================

Introduction to Machine Learning
----------------------------------------------------------------------
  [ ] Lesson  1: Introduction to machine learning
  [ ] Lesson  2: The History of machine learning
  [ ] Lesson  3: Fairness and machine learning
  [ ] Lesson  4: Techniques for machine learning

...

> lesson 5

📚 Lesson 5: Introduction to regression
======================================================================
Status: ⏳ Not Started
Section: Regression
Path: 2-Regression/1-Tools/README.md

What to expect:
  • Pre-lecture warmup quiz
  • Written lesson with examples
  • Hands-on project or exercises
  • Knowledge checks
  • Post-lecture quiz
  • Assignment

💡 Tip: Navigate to '2-Regression/1-Tools' to start the lesson!
======================================================================

> mark 5

✓ Lesson 5 marked as completed! Keep up the great work! 🎉

> progress

📊 Your Learning Progress
======================================================================
Completed: 1/26 lessons (3.8%)
Progress: [█░░░░░░░░░░░░░░░░░░░] 3.8%

✓ Completed Lessons:
  • Lesson 5: Introduction to regression

⏳ Remaining Lessons:
  25 lessons to go!
======================================================================

> recommend

💡 Recommended Next Lesson:
======================================================================
Lesson 1: Introduction to machine learning
Section: Introduction to Machine Learning
Path: 1-Introduction/1-intro-to-ML/README.md

This lesson follows the natural progression of the curriculum.
======================================================================

> search nlp

🔍 Search results for 'nlp':
======================================================================
  [ ] Lesson 16: Introduction to NLP
      Section: Natural Language Processing
  [ ] Lesson 17: Common NLP Tasks
      Section: Natural Language Processing
  [ ] Lesson 18: Translation and sentiment analysis
      Section: Natural Language Processing
...
======================================================================

> quit

👋 Thank you for using the ML Course Agent! Happy learning!
```

## Features in Detail

### Progress Tracking

The agent automatically saves your progress to a local file (`.ml_agent_progress.json`) so you can:
- Keep track of completed lessons
- Resume your learning journey anytime
- Visualize your overall progress with a progress bar

### Smart Recommendations

Based on your progress, the agent recommends:
- The next logical lesson in the curriculum sequence
- Lessons you haven't completed yet
- Topic-specific recommendations

### Interactive Search

Search capabilities include:
- Keyword search across lesson titles
- Topic-based filtering
- Section-wide browsing

## Technical Details

### Architecture

The agent is built using:
- **Pure Python**: No external dependencies required
- **Object-Oriented Design**: Clean, maintainable code structure
- **JSON Storage**: Simple file-based progress persistence
- **Interactive CLI**: User-friendly command-line interface

### File Structure

```
ml_course_agent.py          # Main agent application
.ml_agent_progress.json     # Auto-generated progress file (git-ignored)
ML_COURSE_AGENT.md          # This documentation
```

### Progress File Format

The agent stores progress in JSON format:
```json
{
  "progress": {
    "1": true,
    "5": true,
    "10": false
  },
  "last_updated": "2025-10-20T06:31:50.000000"
}
```

## Tips for Students

1. **Start with `list`**: Get an overview of all available lessons
2. **Use `recommend`**: Follow the recommended learning path
3. **Mark lessons**: Use `mark` to track your progress and stay motivated
4. **Search often**: Use `search` to find specific topics you're interested in
5. **Check resources**: Use `resources` to access additional materials

## Integration with Course

The agent complements the course by:
- Providing quick navigation without opening multiple files
- Tracking progress across the entire curriculum
- Offering a centralized hub for course information
- Making it easier to plan your learning journey

## Extending the Agent

The agent is designed to be extensible. Future enhancements could include:
- Integration with quiz app
- Personalized study plans
- Time tracking
- Integration with GitHub for automatic progress updates
- AI-powered Q&A about lesson content
- Spaced repetition reminders

## Troubleshooting

### Progress not saving
- Ensure you have write permissions in the current directory
- Check that `.ml_agent_progress.json` is not read-only

### Command not recognized
- Type `help` to see all available commands
- Commands are case-insensitive
- Use exact command names as listed

### Python version issues
- Ensure Python 3.6 or higher is installed
- Check with: `python --version` or `python3 --version`

## Contributing

To contribute to the agent:
1. Fork the repository
2. Make your changes to `ml_course_agent.py`
3. Test thoroughly with various commands
4. Submit a pull request with clear description

## License

This agent is part of the ML for Beginners curriculum and follows the same MIT License.

## Support

For issues or questions:
- Open an issue on GitHub
- Check the main course README
- Visit the Discussion Board

## Acknowledgments

Built to support the excellent **Machine Learning for Beginners** curriculum created by Microsoft Cloud Advocates and contributors.

---

**Happy Learning! 🚀📚**
