
# Dodge 'Em Game

This project is a recreation of the classic Atari game **Dodge 'Em**, developed using **Python** and **Pygame**. The entire codebase was generated by **OpenAI's strawberry model "o1-preview"**—no human intervention was involved in writing or debugging any line of code.

## Overview

In this game, the player controls a car moving counterclockwise on a four-lane track, collecting dots and avoiding collisions with an AI-controlled car that chases the player. The challenge lies in switching lanes at the right moments while collecting all the dots and evading the AI car.

## Features

- **Four-Lane Track**: Navigate through a square track with four concentric lanes.
- **Player Car**: Controlled using left and right arrow keys to change lanes and avoid collisions.
- **AI Car**: The AI follows a fixed pattern and starts chasing the player after a few laps.
- **Dots**: Collect dots scattered across the lanes to increase your score.
- **Lane Switching**: Change lanes only when you're at a gap located on the track's sides.

## How It Was Built

This project was **entirely created using OpenAI's strawberry model "o1-preview"**, which generated all the code, including game logic, event handling, and car behavior. The process involved multiple iterations to refine the mechanics, and the AI model provided solutions for handling complex behaviors such as lane transitions and AI chasing logic.

## Installation

To get started with this game, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/niazikashif/Dodge-Em-Atari-ChatGPT.git
   cd dodge-em-game
   ```

2. **Install the required dependencies**:
   ```bash
   pip install pygame
   ```

3. **Run the game**:
   ```bash
   python main.py
   ```

## Game Controls

- **Left Arrow**: Move to an inward lane (when at a gap).
- **Right Arrow**: Move to an outward lane (when at a gap).
- **Spacebar**: Speed boost.

## Development Insights

Working with OpenAI's **o1-preview** model provided unique insights into the capabilities of AI in software development:

- **What Worked**: 
   - The AI was effective in setting up the foundational game logic and managing basic event handling.
   - Initial lane transition, scoring, and car movement were implemented quickly with minimal issues.
   
- **Challenges**:
   - The AI hallucinated several times, generating illogical car movements and lane transition logic that led to erratic behavior, such as cars skipping tracks or jumping across the map.
   - Ensuring smooth lane transitions and proper car behavior at corners required extensive iteration and debugging.
   
- **Conclusion**: 
   - While **o1-preview** is an impressive tool for automating development, certain areas—especially those involving real-time event handling and game mechanics—require human oversight and fine-tuning.


## Contributions

Since this game was built entirely by AI, contributions from the open-source community are highly encouraged! Feel free to fork the repo, submit pull requests, and suggest new features or improvements.

---

## Acknowledgments

A special thanks to **OpenAI** for providing the **strawberry model "o1-preview"**, which generated all the code in this project without human-written code.
