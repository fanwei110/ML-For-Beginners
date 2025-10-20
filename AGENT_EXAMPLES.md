# ML Course Agent - Usage Examples

This document provides practical examples of using the ML Course Agent.

## Quick Start

### Starting the Agent

```bash
# Navigate to the repository root
cd ML-For-Beginners

# Run the agent
python ml_course_agent.py
```

## Example Session

Here's a complete example session showing common workflows:

### 1. First Time User - Getting Started

```
> help
📚 Available Commands:
----------------------------------------------------------------------
  list              - Show all course topics and lessons
  lesson <num>      - Get details about a specific lesson
  topic <name>      - Show all lessons in a topic
  search <keyword>  - Search for lessons by keyword
  progress          - View your learning progress
  mark <num>        - Mark a lesson as completed
  recommend         - Get a lesson recommendation
  quiz              - Get information about quizzes
  resources         - Show additional learning resources
----------------------------------------------------------------------

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
```

### 2. Exploring a Topic

```
> topic nlp
📖 Natural Language Processing
======================================================================
  [ ] Lesson 16: Introduction to NLP
  [ ] Lesson 17: Common NLP Tasks
  [ ] Lesson 18: Translation and sentiment analysis
  [ ] Lesson 19: Romantic hotels of Europe (Sentiment)
  [ ] Lesson 20: Romantic hotels of Europe (Embeddings)
======================================================================
```

### 3. Getting Lesson Details

```
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
```

### 4. Searching for Topics

```
> search classification
🔍 Search results for 'classification':
======================================================================
  [ ] Lesson 10: Introduction to classification
      Section: Classification
  [ ] Lesson 11: Delicious Asian and Indian cuisines
      Section: Classification
  [ ] Lesson 12: More delicious Asian cuisines
      Section: Classification
  [ ] Lesson 13: Build a recommender system
      Section: Classification
======================================================================
```

### 5. Tracking Progress

```
> mark 1
✓ Lesson 1 marked as completed! Keep up the great work! 🎉

> mark 5
✓ Lesson 5 marked as completed! Keep up the great work! 🎉

> progress
📊 Your Learning Progress
======================================================================
Completed: 2/26 lessons (7.7%)
Progress: [█░░░░░░░░░░░░░░░░░░░] 7.7%

✓ Completed Lessons:
  • Lesson 1: Introduction to machine learning
  • Lesson 5: Introduction to regression

⏳ Remaining Lessons:
  24 lessons to go!
======================================================================
```

### 6. Getting Recommendations

```
> recommend
💡 Recommended Next Lesson:
======================================================================
Lesson 2: The History of machine learning
Section: Introduction to Machine Learning
Path: 1-Introduction/2-history-of-ML/README.md

This lesson follows the natural progression of the curriculum.
======================================================================
```

### 7. Quiz Information

```
> quiz
📝 Quiz Information
======================================================================
The course includes 52 quizzes (pre- and post-lecture quizzes).

Quiz Features:
  • Each quiz contains 3 questions
  • Pre-lecture quizzes prepare you for the lesson
  • Post-lecture quizzes test your understanding
  • Interactive quiz app available in /quiz-app folder

To use the quiz app locally:
  1. cd quiz-app
  2. npm install
  3. npm run serve

Quizzes are also available online at: https://aka.ms/ml-beginners
======================================================================
```

### 8. Additional Resources

```
> resources
📚 Additional Resources
======================================================================
Microsoft Learn Collections:
  • Main collection: https://learn.microsoft.com/collections/qrqzamz1nn2wx3

Video Resources:
  • ML for Beginners Playlist: https://aka.ms/ml-beginners-videos

Related Curricula:
  • Data Science for Beginners: https://aka.ms/ds4beginners
  • AI for Beginners: https://aka.ms/ai4beginners

Community:
  • Discussion Board: GitHub Discussions
  • GitHub Issues: Report bugs or request features

Tools & Libraries:
  • Python, Scikit-learn, Pandas, Matplotlib
  • R available for some lessons
  • Jupyter Notebooks included
======================================================================
```

## Common Workflows

### Starting Your Learning Journey

1. Run `list` to see all available lessons
2. Run `lesson 1` to get details about the first lesson
3. Complete Lesson 1
4. Run `mark 1` to track your progress
5. Run `recommend` to get the next lesson suggestion

### Finding Specific Topics

1. Run `search <keyword>` to find lessons about a topic
2. Run `topic <name>` to see all lessons in a category
3. Run `lesson <num>` to get full details

### Tracking Your Progress

1. Mark lessons as completed with `mark <num>` after finishing them
2. Run `progress` regularly to see your advancement
3. Use `recommend` to stay on track

### Exploring Advanced Topics

1. Use `search nlp` to find NLP lessons
2. Use `search reinforcement` to find RL lessons
3. Use `topic timeseries` to explore time series forecasting

## Tips and Tricks

### Efficient Navigation

- Use `list` to get a quick overview of all 26 lessons
- Use `topic` when you want to focus on a specific area
- Use `search` when looking for keywords like "pumpkin", "hotel", "cuisine"

### Progress Management

- Mark lessons immediately after completion for accurate tracking
- Check `progress` weekly to see your advancement
- Use the progress bar for visual motivation

### Learning Path

- Follow `recommend` suggestions for optimal learning progression
- Don't skip the Introduction section (Lessons 1-4)
- Track which lessons you've marked to maintain consistency

### Resource Access

- Use `quiz` to understand quiz structure before starting
- Use `resources` to find additional learning materials
- Check lesson paths to navigate directly to lesson folders

## Troubleshooting

### Agent Won't Start

```bash
# Check Python version
python --version  # Should be 3.6+

# Try python3 explicitly
python3 ml_course_agent.py
```

### Progress Not Saving

```bash
# Check if progress file exists
ls -la .ml_agent_progress.json

# Check file permissions
chmod 644 .ml_agent_progress.json
```

### Commands Not Working

- Ensure you're typing commands correctly (case-insensitive)
- Use `help` to see all available commands
- Check for typos in command arguments

## Demo Mode

Want to see all features in action? Run the demo:

```bash
python demo_agent.py
```

This will showcase all major features automatically.

## Integration with Learning

### Before Each Lesson

1. Run `lesson <num>` to see what to expect
2. Check the lesson path
3. Review prerequisites if mentioned

### After Each Lesson

1. Run `mark <num>` to update progress
2. Run `recommend` to see what's next
3. Run `progress` to see overall advancement

### Weekly Review

1. Run `progress` to see completed lessons
2. Run `list` to see remaining lessons
3. Plan next week's learning goals

## Advanced Usage

### Batch Operations

You can create a script to mark multiple lessons:

```bash
# Create a file with commands
cat > commands.txt << EOF
mark 1
mark 2
mark 3
progress
quit
EOF

# Run the agent with the commands
python ml_course_agent.py < commands.txt
```

### Integration with Scripts

```python
# Example: Using agent in your own script
from ml_course_agent import MLCourseAgent

agent = MLCourseAgent()
agent._load_progress()
agent.list_courses()
```

## Keyboard Shortcuts

- `Ctrl+C`: Exit the agent immediately
- `Ctrl+D`: Exit the agent (EOF)
- `Up Arrow`: Not available (standard input)

## Getting Help

- Type `help` in the agent for command reference
- Read `ML_COURSE_AGENT.md` for detailed documentation
- Read `ML_COURSE_AGENT_CN.md` for Chinese documentation

---

**Happy Learning! 🚀📚**
