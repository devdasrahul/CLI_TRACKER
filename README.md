# 🎯 Personal Tracker CLI - Your All-in-One Life Management System

A comprehensive, crash-free terminal-based tracker for managing every aspect of your life - from habits and goals to health, learning, and finances. Built entirely with Python's standard library.

## ✨ Features

### 📊 20+ Specialized Trackers

#### 🧠 Study & Skill Growth
- **Learning Tracker** - Track subjects, topics, and study hours
- **Project Tracker** - Monitor coding/creative projects with progress bars
- **Reading Tracker** - Log books, papers, and articles with ratings

#### ❤️ Health & Lifestyle
- **Fitness Tracker** - Record workouts, duration, and calories
- **Diet/Meal Tracker** - Monitor meals and calorie intake
- **Sleep Tracker** - Track sleep hours and quality
- **Mood Tracker** - Monitor emotional health with trends

#### 💼 Career & Productivity
- **Goal Tracker** - Set and track long-term goals with deadlines
- **Time Tracker** - Log work sessions with focus ratings
- **Event Tracker** - Manage meetings and reminders
- **Task Tracker** - Organize tasks by priority and status

#### 💰 Financial Management
- **Expense Tracker** - Track spending with category breakdowns
- **Income Tracker** - Log income sources
- **Savings/Budget Tracker** - Monitor budgets and savings goals
- **Shopping List** - Keep track of items to buy

#### 🧘 Mindfulness & Reflection
- **Daily Journal** - Write daily reflections
- **Gratitude Tracker** - Log things you're thankful for

#### 💻 Developer Tools
- **Bug Tracker** - Track and fix coding bugs
- **Code Snippet Tracker** - Save reusable code snippets
- **Interview Prep Tracker** - Prepare for placements
- **Habit Tracker** - Build and maintain habits
- **Task Manager** - General task management

### 🚀 Smart Features

#### 💡 AI-Like Insights (Rule-Based)
- Detects spending increases and provides budget alerts
- Identifies missed habits and workout streaks
- Analyzes mood trends and provides encouragement
- Suggests task prioritization based on pending items
- Calculates study time and focus patterns

#### ⏱️ Focus Mode
- Pomodoro-style timer for focused work
- Automatic logging to Time Tracker
- Focus rating collection after each session

#### 🎨 Customization
- User profiles
- Theme support (default, dark, light, no-color)
- Daily motivational quotes
- Colored terminal output with emoji icons

#### 🔒 Data Safety & Recovery
- **Auto-backup** - Timestamped backup after every update
- **Undo functionality** - Roll back last delete/update
- **Archive system** - Move old entries (30+ days) to archive
- **Backup cleanup** - Keep only last 10 backups
- **Corruption recovery** - Restore from latest backup automatically
- **Activity logging** - Every action logged with timestamp

#### 🔍 Advanced Search & Filter
- Search by keyword across all fields
- Filter by date range (today, this week, custom)
- Filter by specific field values
- Highlighted results

#### 📊 Comprehensive Analytics
- **Habits**: Completion rates and current streaks
- **Tasks**: Status distribution and priority breakdown
- **Expenses**: Total, average, and category analysis
- **Mood**: Weekly trends with encouragement
- **Study**: Total hours per subject with visual bars
- **Fitness**: Workout stats and calorie tracking
- **Goals**: Progress tracking and completion rates
- **Time**: Focus analysis and category breakdown

#### 📤 Export & Reporting
- Export to JSON (all data)
- Export to CSV (per tracker)
- Summary reports (TXT)
- Monthly reports
- Activity log

### 🎮 Quick Commands

Instead of navigating menus, use quick commands:
```
add habit
list expenses
analyze mood
delete task
search reading
```

## 🚀 Getting Started

### Prerequisites
- Python 3.6 or higher
- No external dependencies required!

### Installation

1. Extract the zip file:
```bash
unzip PY_CSE-2025_Rahul_Personal_Tracker.zip
cd PY_CSE-2025_Rahul_Personal_Tracker
```

2. Run the application:
```bash
python app.py
```

Or make it executable (Linux/Mac):
```bash
chmod +x app.py
./app.py
```

## 📖 Usage Guide

### Main Menu
```
1. ➕ Add Entry         - Add new entries to any tracker
2. 📋 List Entries      - View all entries in a tracker
3. ✏️ Update Entry      - Modify existing entries
4. 🗑️ Delete Entry      - Remove entries (with undo)
5. 🔍 Search/Filter     - Find specific entries
6. 📊 Analyze/Insights  - View statistics and trends
7. 📤 Export/Backup     - Export data and manage backups
8. ⏱ Focus Mode        - Pomodoro timer for productivity
9. 🎨 Settings          - Customize app preferences
0. 🚪 Exit              - Save and quit
```

### Adding Entries
1. Select "Add Entry" or use quick command `add habit`
2. Choose your tracker
3. Fill in the required fields
4. Data is automatically saved with backup

### Viewing Analytics
1. Select "Analyze/Insights"
2. Choose a tracker
3. View comprehensive statistics:
   - Total entries and trends
   - Category breakdowns with visual bars
   - Smart suggestions based on your data
   - Streak tracking for habits
   - Spending alerts for expenses

### Using Focus Mode
1. Select "Focus Mode"
2. Enter duration (default: 25 minutes)
3. Specify what you're working on
4. Timer counts down with live display
5. Rate your focus level when complete
6. Session automatically logged to Time Tracker

### Exporting Data
1. Select "Export/Backup/Restore"
2. Choose export format:
   - JSON for complete backup
   - CSV for spreadsheet analysis
   - TXT for readable reports
   - Monthly reports for archiving

## 📁 File Structure

```
Personal_Tracker/
├── app.py              # Main application
├── data.json           # Your data (auto-created)
├── backup/             # Auto-backups (auto-created)
│   ├── backup_20250105_143022.json
│   └── ...
├── archive.json        # Old entries archive
├── log.txt             # Activity log
├── summary.txt         # Latest summary export
└── README.md           # This file
```

## 🎨 Themes

Change themes in Settings menu:
- **default**: Colorful with emojis
- **dark**: Dark-friendly colors
- **light**: Light terminal colors
- **no-color**: Plain text (for compatibility)

## 🔧 Advanced Features

### Undo Functionality
Made a mistake? Use Settings → Undo Last Action to revert:
- Deletes
- Updates

### Archive Old Entries
Keep your main data clean:
- Settings → Archive Old Entries
- Moves entries older than 30 days to archive.json
- Keeps current data fast and manageable

### Backup & Restore
- Automatic backups on every save
- Manual backup: Settings → Backup Data
- Restore: Settings → Restore from Backup
- Keeps last 10 backups automatically

### Data Recovery
If data.json gets corrupted:
1. App automatically detects corruption
2. Restores from latest backup
3. No data loss!

## 💡 Smart Suggestions Examples

The app provides intelligent, context-aware suggestions:

- **Habits**: "You've missed your fitness goal for 3 days. Time to move! 🏃"
- **Expenses**: "You spent 40% more this week — maybe cut down on dining out 🍽️"
- **Mood**: "Mood trend: You've had more 'Happy' entries this week 😊"
- **Goals**: "You have 5 goals with low progress. Break them into smaller tasks!"
- **Tasks**: "You have 12 pending tasks. Prioritize the top 3 for today!"

## 🛡️ Error Handling

The app is built to be crash-free:
- ✅ All inputs are validated
- ✅ Graceful handling of all exceptions
- ✅ No uncaught errors on normal operations
- ✅ Safe file operations with fallbacks
- ✅ Data corruption recovery
- ✅ Keyboard interrupt handling

## 📊 Example Analytics Output

### Expense Tracker Analysis
```
📊 Analysis for Expense Tracker
================================================
📈 Total Entries: 24
💰 Total Expenses: $1,847.50
🏷️ Categories: 5

📊 Expenses by Category:
  Food: $685.00 (37.1%) ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Transport: $420.00 (22.7%) ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Entertainment: $380.50 (20.6%) ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Shopping: $242.00 (13.1%) ▓▓▓▓▓▓▓▓▓▓
  Bills: $120.00 (6.5%) ▓▓▓▓

📈 Average Expense: $76.98

💡 Smart Suggestions:
  ⚠️ Spending increased by 30% this week. Consider reviewing your budget!
```

### Learning Tracker Analysis
```
📊 Analysis for Learning Tracker
================================================
📈 Total Entries: 18
⏱️ Total Study Hours: 45.5
📚 Subjects Covered: 4

📊 Hours by Subject:
  Python: 15.0h ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Data Structures: 12.5h ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Web Dev: 10.0h ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
  Algorithms: 8.0h ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓

💡 Smart Suggestions:
  🎉 Great consistency! You're on fire!
```

## 🎯 Use Cases

### For Students
- Track study hours and subjects
- Monitor project progress
- Prepare for interviews
- Manage deadlines and tasks
- Track reading assignments

### For Developers
- Log bugs and fixes
- Save code snippets
- Track coding projects
- Monitor focus time
- Prepare for technical interviews

### For Everyone
- Build healthy habits
- Track fitness and diet
- Monitor mood and wellbeing
- Manage finances
- Set and achieve goals
- Practice gratitude

## 🏆 Key Highlights

- **20+ trackers** covering all life areas
- **100% Python standard library** - no dependencies
- **Completely crash-free** - robust error handling
- **Auto-backup system** - never lose data
- **Smart insights** - rule-based AI suggestions
- **Quick commands** - fast navigation
- **Export flexibility** - JSON, CSV, TXT
- **Focus timer** - Pomodoro built-in
- **Visual analytics** - progress bars and charts
- **Undo functionality** - rollback mistakes
- **Archive system** - keep data organized
- **Activity logging** - full audit trail

## 🤝 Acknowledgments

This project was developed as part of the Python CSE Challenge 2025. AI assistance (Claude) was used for code structure planning and best practices guidance.

## 📝 License

This project is for educational purposes as part of the CSE Python Challenge.

## 👨‍💻 Author

**Rahul AND MANAV SHARMA** - CSE Student

---
## AI Assistance Disclosure

This project was built using Python's standard library only. AI assistance was used for idea structuring, code organization, and documentation to ensure best practices and comprehensive error handling.

**Made with ❤️ and Python's Standard Library**

*"The secret of getting ahead is getting started." - Mark Twain*