import type { PageLoad } from "./$types";

export const load: PageLoad = async ({ params, fetch }) => {
  const gameId = params.gameId;

  // This function fetches the entire game state, which now includes
  // the nested dynasty object thanks to our backend changes.
  async function fetchGameData() {
    const response = await fetch(
      `http://localhost:8000/api/v1/games/${gameId}`
    );
    if (!response.ok) throw new Error(`Failed to fetch game session`);
    return response.json();
  }

  // This function fetches the current decision for the player
  async function fetchDecisionNode(decisionNodeId: number | null) {
    if (!decisionNodeId) {
      // If there's no current decision, we don't need to fetch anything.
      return null;
    }
    const response = await fetch(
      `http://localhost:8000/api/v1/decisions/${decisionNodeId}`
    );
    if (!response.ok) throw new Error(`Failed to fetch decision node`);
    return response.json();
  }

  // First, get the game data
  const game = await fetchGameData();

  // Then, use the ID from the game data to fetch the correct decision node
  const decisionNode = await fetchDecisionNode(game.current_decision_node_id);

  // Return all data to the component
  return {
    game: game,
    decisionNode: decisionNode,
  };
};
