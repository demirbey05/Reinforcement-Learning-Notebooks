import torch
from typing import List, Union

class MDP:
    def __init__(
            self,
            states: List[Union[int, str]],
            actions: List[Union[int, str]],
            transition_model: torch.Tensor
        ) -> None:
        '''
        Args:
            states: list of states, can be integers or strings
            actions: list of actions, can be integers or strings
            transition_model: tensor of shape (n, 5) where each row contains
                            [current_state, action, next_state, reward, probability]
        '''
        self.states = states
        self.actions = actions
        # Ensure the transition model is a torch tensor
        self.transition_model = transition_model if torch.is_tensor(transition_model) \
            else torch.tensor(transition_model, dtype=torch.float32)

    def get_probability(self, current_state: Union[int, str], action: Union[int, str], 
                       next_state: Union[int, str], reward: float) -> float:
        '''
        Get the probability of transitioning from current_state to next_state
        with the given action and reward.
        
        Args:
            current_state: current state
            action: action taken
            next_state: next state
            reward: reward received for the transition
        Returns:
            probability: probability of transitioning from current state to next state
                        with the given action and reward. Returns 0 if transition not found.
        '''
        # Find matching transitions in the transition model using torch operations
        mask = torch.logical_and(
            torch.logical_and(
                self.transition_model[:, 0] == current_state,
                self.transition_model[:, 1] == action
            ),
            torch.logical_and(
                self.transition_model[:, 2] == next_state,
                self.transition_model[:, 3] == reward
            )
        )
        
        # If matching transition found, return its probability
        if torch.any(mask):
            return float(self.transition_model[mask][0, 4])
        
        # If no matching transition found, return 0
        return 0.0

    def get_next_states(self, current_state: Union[int, str], 
                       action: Union[int, str]) -> torch.Tensor:
        '''
        Get all possible next states and their probabilities for a given state-action pair.
        
        Args:
            current_state: current state
            action: action taken
        Returns:
            next_states_info: tensor containing [next_state, reward, probability]
        '''
        # Find all transitions for the given state-action pair
        mask = torch.logical_and(
            self.transition_model[:, 0] == current_state,
            self.transition_model[:, 1] == action
        )
        
        # Return the next states, rewards, and probabilities
        if torch.any(mask):
            return self.transition_model[mask][:, 2:]  # Returns columns [next_state, reward, probability]
        
        return torch.empty(0, 3)  # Return empty tensor if no transitions found
