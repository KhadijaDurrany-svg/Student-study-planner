import streamlit as st
import json
import os
import random
from datetime import datetime, date, time, timedelta

# Auto refresh for Focus Mode
try:
    from streamlit_autorefresh import st_autorefresh
    AUTO_REFRESH_AVAILABLE = True
except ImportError:
    AUTO_REFRESH_AVAILABLE = False


# --------------------------------------------------
# APP SETTINGS
# --------------------------------------------------

st.set_page_config(
    page_title="Student Study Planner",
    page_icon="📚",
    layout="centered"
)

FILE_NAME = "study_tasks.json"


# --------------------------------------------------
# MOTIVATIONAL MESSAGES
# --------------------------------------------------

MOTIVATIONAL_MESSAGES = [
    "💪 Great job! Keep going!",
    "🌟 You are getting closer to your goals!",
    "📚 Every minute of learning matters.",
    "🚀 Stay focused. You will become what you dream of.",
    "💡 Learn a skill today that your future self will thank you for.",
    "🔥 Don't give up. Small progress is still progress!",
    "🎯 Focus on your goal, not the distraction.",
    "🌱 One task at a time. You can do it!",
    "✨ Your future is built by what you do today.",
    "🏆 Great work! Keep building your skills!",
    "💻 Keep learning. Your skills can create your future.",
    "🌸 Small steps every day create big results.",
    "🧠 Keep your mind busy with learning, not distractions.",
    "⭐ You don't need to be perfect. Just keep improving."
]


SKILL_MESSAGES = [
    "💻 Learn Python today.",
    "🤖 Learn one AI tool today.",
    "🔐 Learn one cybersecurity concept today.",
    "🧠 Learn something new for 30 minutes.",
    "📖 Improve your English speaking today.",
    "🌐 Learn one useful technology skill today.",
    "🐍 Practice Python instead of scrolling.",
    "🚀 Build a small project today.",
    "💡 Learn a skill that can help your future career."
]


DISTRACTION_MESSAGES = [
    "📵 You opened a distraction. Come back to your goal!",
    "⏳ Don't waste your valuable study time.",
    "🎯 Your goal is more important than scrolling.",
    "📚 Put the phone away and focus on your task.",
    "🚀 Future you will thank you for studying now.",
    "💪 Stay focused. You are building your future."
]


# --------------------------------------------------
# LOAD / SAVE TASKS
# --------------------------------------------------

def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []

    return []


def save_tasks():
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(st.session_state.tasks, file, indent=4)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()

if "focus_running" not in st.session_state:
    st.session_state.focus_running = False

if "focus_start" not in st.session_state:
    st.session_state.focus_start = None

if "focus_minutes" not in st.session_state:
    st.session_state.focus_minutes = 25

if "daily_goal" not in st.session_state:
    st.session_state.daily_goal = 120


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📚 Student Study Planner")

st.write(
    "Plan your study, complete your tasks, stay focused "
    "and build useful skills. 🚀"
)

st.divider()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.title("⚙️ Settings")


# Daily goal
st.sidebar.header("🎯 Daily Study Goal")

daily_goal = st.sidebar.number_input(
    "Goal in minutes",
    min_value=15,
    max_value=1000,
    value=st.session_state.daily_goal,
    step=15
)

st.session_state.daily_goal = daily_goal


# Night mode
st.sidebar.header("🌙 Night Screen-Time Mode")

night_mode = st.sidebar.checkbox(
    "Enable Night Mode"
)

if night_mode:

    sleep_time = st.sidebar.time_input(
        "Sleep time",
        value=time(22, 0)
    )

    wake_time = st.sidebar.time_input(
        "Wake-up time",
        value=time(7, 0)
    )

    current_time = datetime.now().time()

    if sleep_time <= wake_time:
        night_active = (
            sleep_time <= current_time <= wake_time
        )
    else:
        night_active = (
            current_time >= sleep_time
            or current_time <= wake_time
        )

    if night_active:

        st.sidebar.warning(
            "🌙 Screen-free time is active!"
        )

        st.warning(
            "🌙 It's your screen-free time. "
            "Put your phone away, rest your eyes "
            "and get ready for sleep. 😴"
        )

        st.info(
            "💡 Your future needs rest too. "
            "Sleep well and come back stronger tomorrow!"
        )


# Motivation button
st.sidebar.header("💬 Motivation")

if st.sidebar.button("💪 Give Me Motivation"):

    st.sidebar.success(
        random.choice(MOTIVATIONAL_MESSAGES)
    )


# Skill button
if st.sidebar.button("💡 Skill of the Day"):

    st.sidebar.info(
        random.choice(SKILL_MESSAGES)
    )


# Distraction reminder
if st.sidebar.button("📵 I am getting distracted"):

    st.sidebar.warning(
        random.choice(DISTRACTION_MESSAGES)
    )


# --------------------------------------------------
# ADD TASK
# --------------------------------------------------

st.header("➕ Add Study Task")

with st.form("task_form"):

    subject = st.text_input(
        "📚 Subject",
        placeholder="Example: Python"
    )

    task_name = st.text_input(
        "📝 Study Task",
        placeholder="Example: Practice loops"
    )

    task_date = st.date_input(
        "📅 Date",
        value=date.today()
    )

    study_time = st.number_input(
        "⏱️ Study Time (minutes)",
        min_value=1,
        max_value=600,
        value=30
    )

    priority = st.selectbox(
        "⭐ Priority",
        ["Low", "Medium", "High"]
    )

    reminder = st.time_input(
        "🔔 Reminder Time",
        value=time(18, 0)
    )

    add_task = st.form_submit_button(
        "➕ Add Task"
    )


    if add_task:

        if subject.strip() == "" or task_name.strip() == "":

            st.error(
                "Please enter both Subject and Study Task."
            )

        else:

            new_task = {
                "id": datetime.now().timestamp(),
                "subject": subject.strip(),
                "task": task_name.strip(),
                "date": str(task_date),
                "study_time": study_time,
                "priority": priority,
                "reminder": reminder.strftime("%H:%M"),
                "completed": False,
                "completed_at": ""
            }

            st.session_state.tasks.append(new_task)

            save_tasks()

            st.success(
                "✅ Task added successfully!"
            )

            st.info(
                random.choice(MOTIVATIONAL_MESSAGES)
            )


st.divider()


# --------------------------------------------------
# TODAY'S REMINDERS
# --------------------------------------------------

current_date = str(date.today())
current_time = datetime.now().strftime("%H:%M")

for task in st.session_state.tasks:

    if (
        task.get("date") == current_date
        and task.get("reminder") == current_time
        and not task.get("completed", False)
    ):

        st.warning(
            f"🔔 Reminder: Time to study "
            f"{task.get('subject')} — "
            f"{task.get('task')}"
        )


# --------------------------------------------------
# TODAY'S STATISTICS
# --------------------------------------------------

today_tasks = [
    task
    for task in st.session_state.tasks
    if task.get("date") == current_date
]


today_completed = [
    task
    for task in today_tasks
    if task.get("completed", False)
]


today_total_minutes = sum(
    int(task.get("study_time", 0))
    for task in today_completed
)


today_planned_minutes = sum(
    int(task.get("study_time", 0))
    for task in today_tasks
)


# --------------------------------------------------
# PROGRESS
# --------------------------------------------------

st.header("📊 Your Progress")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Today's Tasks",
        len(today_tasks)
    )

with col2:
    st.metric(
        "Completed",
        len(today_completed)
    )

with col3:
    st.metric(
        "Study Minutes",
        today_total_minutes
    )


if daily_goal > 0:

    goal_progress = min(
        today_total_minutes / daily_goal,
        1.0
    )

    st.write(
        f"🎯 Daily Goal: "
        f"{today_total_minutes}/{daily_goal} minutes"
    )

    st.progress(goal_progress)

    if today_total_minutes >= daily_goal:

        st.success(
            "🏆 Amazing! You reached your daily study goal!"
        )

    else:

        remaining_goal = daily_goal - today_total_minutes

        st.info(
            f"📚 Only {remaining_goal} more minutes "
            f"to reach today's goal!"
        )


st.divider()


# --------------------------------------------------
# TASK FILTER
# --------------------------------------------------

st.header("📋 Your Study Tasks")

filter_option = st.selectbox(
    "🔎 Show Tasks",
    [
        "All Tasks",
        "Today's Tasks",
        "Completed",
        "Not Completed",
        "High Priority"
    ]
)


filtered_tasks = []

for task in st.session_state.tasks:

    if filter_option == "All Tasks":

        filtered_tasks.append(task)

    elif filter_option == "Today's Tasks":

        if task.get("date") == current_date:
            filtered_tasks.append(task)

    elif filter_option == "Completed":

        if task.get("completed", False):
            filtered_tasks.append(task)

    elif filter_option == "Not Completed":

        if not task.get("completed", False):
            filtered_tasks.append(task)

    elif filter_option == "High Priority":

        if task.get("priority") == "High":
            filtered_tasks.append(task)


# --------------------------------------------------
# DISPLAY TASKS
# --------------------------------------------------

if len(filtered_tasks) == 0:

    st.info(
        "📚 No tasks found. Add a study task above!"
    )

else:

    for task in filtered_tasks:

        original_index = st.session_state.tasks.index(task)

        if task.get("completed", False):

            status = "✅ Completed"

        else:

            status = "⏳ Not Completed"


        with st.container(border=True):

            st.subheader(
                f"📚 {task.get('subject', 'Subject')}"
            )

            st.write(
                f"📝 **Task:** {task.get('task', '')}"
            )

            st.write(
                f"📅 **Date:** {task.get('date', '')}"
            )

            st.write(
                f"⏱️ **Study Time:** "
                f"{task.get('study_time', 0)} minutes"
            )

            st.write(
                f"⭐ **Priority:** "
                f"{task.get('priority', 'Medium')}"
            )

            st.write(
                f"🔔 **Reminder:** "
                f"{task.get('reminder', '')}"
            )

            st.write(
                f"📌 **Status:** {status}"
            )


            # -----------------------------
            # BUTTONS
            # -----------------------------

            col1, col2, col3 = st.columns(3)


            # Complete
            with col1:

                if not task.get("completed", False):

                    if st.button(
                        "✅ Complete",
                        key=f"complete_{task.get('id')}"
                    ):

                        task["completed"] = True

                        task["completed_at"] = (
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M"
                            )
                        )

                        save_tasks()

                        st.success(
                            "🎉 Great job! Task completed!"
                        )

                        st.info(
                            random.choice(
                                MOTIVATIONAL_MESSAGES
                            )
                        )

                        st.rerun()


            # Delete
            with col2:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_{task.get('id')}"
                ):

                    st.session_state.tasks.pop(
                        original_index
                    )

                    save_tasks()

                    st.success(
                        "🗑️ Task deleted."
                    )

                    st.rerun()


            # Edit
            with col3:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_{task.get('id')}"
                ):

                    st.session_state[
                        f"editing_{task.get('id')}"
                    ] = True

                    st.rerun()


            # -----------------------------
            # EDIT FORM
            # -----------------------------

            if st.session_state.get(
                f"editing_{task.get('id')}",
                False
            ):

                st.write("✏️ **Edit Task**")

                new_subject = st.text_input(
                    "Subject",
                    value=task.get("subject", ""),
                    key=f"subject_edit_{task.get('id')}"
                )

                new_task = st.text_input(
                    "Task",
                    value=task.get("task", ""),
                    key=f"task_edit_{task.get('id')}"
                )

                try:
                    new_date = date.fromisoformat(
                        task.get("date")
                    )
                except:
                    new_date = date.today()

                new_date = st.date_input(
                    "Date",
                    value=new_date,
                    key=f"date_edit_{task.get('id')}"
                )

                new_time = st.number_input(
                    "Study Time",
                    min_value=1,
                    max_value=600,
                    value=int(
                        task.get("study_time", 30)
                    ),
                    key=f"time_edit_{task.get('id')}"
                )

                new_priority = st.selectbox(
                    "Priority",
                    ["Low", "Medium", "High"],
                    index=[
                        "Low",
                        "Medium",
                        "High"
                    ].index(
                        task.get("priority", "Medium")
                    ),
                    key=f"priority_edit_{task.get('id')}"
                )

                try:
                    old_reminder = datetime.strptime(
                        task.get("reminder", "18:00"),
                        "%H:%M"
                    ).time()
                except:
                    old_reminder = time(18, 0)

                new_reminder = st.time_input(
                    "Reminder",
                    value=old_reminder,
                    key=f"reminder_edit_{task.get('id')}"
                )


                save_edit = st.button(
                    "💾 Save Changes",
                    key=f"save_edit_{task.get('id')}"
                )


                if save_edit:

                    task["subject"] = new_subject.strip()
                    task["task"] = new_task.strip()
                    task["date"] = str(new_date)
                    task["study_time"] = new_time
                    task["priority"] = new_priority
                    task["reminder"] = (
                        new_reminder.strftime("%H:%M")
                    )

                    save_tasks()

                    st.session_state[
                        f"editing_{task.get('id')}"
                    ] = False

                    st.success(
                        "✅ Task updated successfully!"
                    )

                    st.rerun()


st.divider()


# --------------------------------------------------
# FOCUS MODE
# --------------------------------------------------

st.header("🎯 Focus Mode")

st.write(
    "Start a focused study session and avoid distractions."
)

focus_minutes = st.selectbox(
    "⏱️ Choose Focus Session",
    [15, 25, 30, 45, 60, 90]
)


if not st.session_state.focus_running:

    if st.button(
        "▶️ Start Focus Session"
    ):

        st.session_state.focus_start = (
            datetime.now()
        )

        st.session_state.focus_minutes = (
            focus_minutes
        )

        st.session_state.focus_running = True

        st.success(
            "🎯 Focus Mode started!"
        )

        st.info(
            "📵 Stay away from Instagram, YouTube, "
            "Facebook and other distractions."
        )

        st.rerun()


else:

    # Auto refresh every second
    if AUTO_REFRESH_AVAILABLE:

        st_autorefresh(
            interval=1000,
            key="focus_timer"
        )


    start_time = st.session_state.focus_start

    end_time = (
        start_time
        + timedelta(
            minutes=st.session_state.focus_minutes
        )
    )

    remaining = (
        end_time - datetime.now()
    )


    if remaining.total_seconds() > 0:

        total_seconds = int(
            remaining.total_seconds()
        )

        minutes_left = total_seconds // 60

        seconds_left = total_seconds % 60


        st.success(
            "🎯 FOCUS MODE IS ON"
        )

        st.metric(
            "Time Remaining",
            f"{minutes_left:02d}:{seconds_left:02d}"
        )

        st.warning(
            random.choice(DISTRACTION_MESSAGES)
        )

        st.write(
            "📚 Work on your study task. "
            "Don't check social media."
        )


        if not AUTO_REFRESH_AVAILABLE:

            st.info(
                "Click the button below to refresh "
                "the timer."
            )

            if st.button(
                "🔄 Refresh Timer"
            ):

                st.rerun()


        if st.button(
            "⏹️ Stop Focus Session"
        ):

            st.session_state.focus_running = False

            st.session_state.focus_start = None

            st.rerun()


    else:

        st.success(
            "🎉 Great job! Your focus session is complete!"
        )

        st.balloons()

        st.info(
            random.choice(
                MOTIVATIONAL_MESSAGES
            )
        )

        st.session_state.focus_running = False

        st.session_state.focus_start = None


st.divider()


# --------------------------------------------------
# STUDY SUMMARY
# --------------------------------------------------

st.header("📈 Study Summary")

total_tasks = len(
    st.session_state.tasks
)

completed_tasks = sum(
    1
    for task in st.session_state.tasks
    if task.get("completed", False)
)

total_planned_minutes = sum(
    int(task.get("study_time", 0))
    for task in st.session_state.tasks
)

total_completed_minutes = sum(
    int(task.get("study_time", 0))
    for task in st.session_state.tasks
    if task.get("completed", False)
)


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "📋 Total Tasks",
        total_tasks
    )

    st.metric(
        "⏱️ Planned Minutes",
        total_planned_minutes
    )

with col2:

    st.metric(
        "✅ Completed Tasks",
        completed_tasks
    )

    st.metric(
        "🎓 Completed Minutes",
        total_completed_minutes
    )


# Completion percentage
if total_tasks > 0:

    completion_percentage = (
        completed_tasks / total_tasks
    ) * 100

    st.write(
        f"🏆 Overall Completion: "
        f"**{completion_percentage:.0f}%**"
    )

    st.progress(
        completion_percentage / 100
    )


# --------------------------------------------------
# STREAK
# --------------------------------------------------

st.header("🔥 Study Streak")

completed_dates = set()

for task in st.session_state.tasks:

    if task.get("completed", False):

        completed_at = task.get(
            "completed_at",
            ""
        )

        if completed_at:

            try:

                completed_day = datetime.strptime(
                    completed_at,
                    "%Y-%m-%d %H:%M"
                ).date()

                completed_dates.add(
                    completed_day
                )

            except:
                pass


streak = 0

check_day = date.today()

while check_day in completed_dates:

    streak += 1

    check_day = (
        check_day - timedelta(days=1)
    )


if streak > 0:

    st.success(
        f"🔥 Your current study streak is "
        f"{streak} day(s)!"
    )

else:

    st.info(
        "🌱 Complete a task today to start "
        "your study streak!"
    )


# --------------------------------------------------
# EXPORT STUDY PLAN
# --------------------------------------------------

st.header("📥 Save Your Study Plan")

if len(st.session_state.tasks) > 0:

    export_data = json.dumps(
        st.session_state.tasks,
        indent=4
    )

    st.download_button(
        label="📥 Download Study Plan",
        data=export_data,
        file_name="my_study_plan.json",
        mime="application/json"
    )


# --------------------------------------------------
# FINAL MOTIVATION
# --------------------------------------------------

st.divider()

st.header("💬 Remember")

st.info(
    "🚀 Stay focused. You will become what you dream of.\n\n"
    "💡 Learn a skill today that your future self "
    "will thank you for.\n\n"
    "📚 Study a little every day. Small progress "
    "becomes big success.\n\n"
    "💪 Great job! Keep going!"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "📚 Student Study Planner | "
    "Study Smart • Stay Focused • Build Your Future 🚀"
)