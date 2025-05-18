
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="Food Finder Game", layout="centered")
st.title("🍕 Food Finder Game with Greedy Check")

GRID_SIZE = 10
MAX_STEPS = 15

# Initialize state
if "player_pos" not in st.session_state:
    st.session_state.player_pos = [0, 0]
if "food_pos" not in st.session_state:
    st.session_state.food_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
if "steps" not in st.session_state:
    st.session_state.steps = 0
if "greedy_moves" not in st.session_state:
    st.session_state.greedy_moves = []  # Track True/False for each move


# Distance helper
def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


# Display grid
def display_grid():
    plt.clf()
    grid = np.ones((GRID_SIZE, GRID_SIZE, 3), dtype=int) * 255

    fx, fy = st.session_state.food_pos
    grid[fy, fx] = [255, 0, 0]

    px, py = st.session_state.player_pos
    grid[py, px] = [0, 255, 0]

    plt.imshow(grid.astype(np.uint8))
    plt.xticks([]);
    plt.yticks([])
    plt.title(f"Steps: {st.session_state.steps}/{MAX_STEPS}")
    st.pyplot(plt.gcf())


# Movement function with greedy check
def move(direction):
    if st.session_state.steps >= MAX_STEPS or st.session_state.player_pos == st.session_state.food_pos:
        return

    old_pos = st.session_state.player_pos[:]
    old_dist = manhattan_distance(old_pos, st.session_state.food_pos)

    x, y = old_pos
    if direction == 'up' and y > 0:
        y -= 1
    elif direction == 'down' and y < GRID_SIZE - 1:
        y += 1
    elif direction == 'left' and x > 0:
        x -= 1
    elif direction == 'right' and x < GRID_SIZE - 1:
        x += 1

    new_pos = [x, y]
    new_dist = manhattan_distance(new_pos, st.session_state.food_pos)
    st.session_state.player_pos = new_pos
    st.session_state.steps += 1

    # Greedy check
    was_greedy = new_dist < old_dist
    st.session_state.greedy_moves.append(was_greedy)

    # Feedback to player
    if was_greedy:
        st.info("✅ That was a **greedy move**.")
    else:
        st.warning("❌ That was **not** a greedy move.")


# Greedy bot move
def greedy_move():
    if st.session_state.steps >= MAX_STEPS or st.session_state.player_pos == st.session_state.food_pos:
        return

    px, py = st.session_state.player_pos
    fx, fy = st.session_state.food_pos

    if px < fx:
        px += 1
    elif px > fx:
        px -= 1
    elif py < fy:
        py += 1
    elif py > fy:
        py -= 1

    st.session_state.player_pos = [px, py]
    st.session_state.steps += 1
    st.session_state.greedy_moves.append(True)  # Bot always moves greedily


# UI
def display_ui():
    display_grid()

    if st.session_state.player_pos == st.session_state.food_pos:
        st.success(f"You reached the food in {st.session_state.steps} steps. 🎉")
        if all(st.session_state.greedy_moves):
            st.success("You followed a **greedy path** all the way! 🧠✅")
        else:
            st.warning("You reached the goal but **deviated from greedy path**. 🤔")

        if st.button("Restart"):
            reset_game()

    elif st.session_state.steps >= MAX_STEPS:
        st.error("⏱️ Out of moves! Try again.")
        if st.button("Restart"):
            reset_game()
    else:
        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("⬆️ Up"):
                move("up")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("⬅️ Left"):
                move("left")
        with col2:
            if st.button("⬇️ Down"):
                move("down")
        with col3:
            if st.button("➡️ Right"):
                move("right")

        st.markdown("### 🤖 Auto Move (Greedy)")
        if st.button("Make Greedy Move"):
            greedy_move()


# Reset game
def reset_game():
    st.session_state.player_pos = [0, 0]
    st.session_state.food_pos = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    st.session_state.steps = 0
    st.session_state.greedy_moves = []


# Start game
display_ui()
