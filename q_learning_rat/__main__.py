from q_learning_rat.agent.deep_q_learning_agent import DeepQLearningAgent
from q_learning_rat.agent.input_agent import InputAgent
from q_learning_rat.agent.q_table_agent import QTableAgent
from q_learning_rat.model.level import Level
from q_learning_rat.view.basic_trainer import BasicTrainer
from q_learning_rat.view.game import Game


if __name__ == "__main__":
    # agent = QTableAgent()
    agent = DeepQLearningAgent(view_distance=3)
    trainer = BasicTrainer(1, agent, view_distance=3)
    game = Game(trainer, debug=False)
    game.run()