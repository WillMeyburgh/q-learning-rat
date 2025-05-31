# Q-Learning Rat

This project implements a Q-learning agent to train a rat to navigate a maze and find cheese while avoiding traps and holes.

![alt text](<Screenshot from 2025-05-31 16-06-25.png>)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd q-learning-rat
    ```

2.  Install dependencies using Poetry:

    ```bash
    poetry install
    ```

## Usage

### Run the game

To run the game with a pre-trained agent, execute the following command:

```bash
poetry run python q_learning_rat
```

### Train the agent

To train the agent, you can modify the training parameters in `q_learning_rat/__main__.py` and then run the main script.

### Modify Levels

To modify the levels, edit the `q_learning_rat/build_levels.py` file
and run
```bash
poetry run python q_learning_rat/build_levels.py
```

### Controls

*   **Right Arrow**: Next level
*   **Left Arrow**: Previous level
*   **Up Arrow**: Next agent
*   **Down Arrow**: Previous agent
*   **R Key**: Restart current level/agent

## Project Structure

*   `q_learning_rat/`: Contains the main application code.
    *   `__main__.py`: Main script to run the game and train the agent.
    *   `build_levels.py`: Script to define and build the levels.
    *   `input.py`: Handles user input.
    *   `agent/`: Contains the agent implementations.
        *   `abstract_agent.py`: Abstract base class for agents.
        *   `deep_q_learning_agent.py`: Deep Q-learning agent implementation.
        *   `input_agent.py`: Agent controlled by user input.
        *   `q_table_agent.py`: Q-table agent implementation.
    *   `model/`: Contains the data model definitions.
        *   `level.py`: Defines the Level class.
        *   `move.py`: Defines the Move enum.
        *   `position.py`: Defines the Position class.
    *   `view/`: Contains the view components.
        *   `basic_trainer.py`: Basic trainer implementation.
        *   `game.py`: Implements the main game loop and rendering.
        *   `level_renderer.py`: Renders the level.
*   `levels/`: Contains the serialized level data.
*   `sprites/`: Contains the image sprites for the game.
