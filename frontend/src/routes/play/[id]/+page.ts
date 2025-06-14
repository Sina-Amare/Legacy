import type { PageLoad } from "./$types";
import type { Dynasty } from "$lib/types";

/**
 * This load function runs before the page component is rendered.
 * It fetches the data needed for this specific dynasty page.
 */
export const load: PageLoad = async ({ params, fetch }) => {
  const dynastyId = params.id;
  const response = await fetch(
    `http://localhost:8000/api/v1/dynasties/${dynastyId}`
  );

  if (!response.ok) {
    throw new Error(`Failed to fetch dynasty with ID ${dynastyId}`);
  }

  const dynasty: Dynasty = await response.json();

  return {
    dynasty: dynasty,
  };
};
